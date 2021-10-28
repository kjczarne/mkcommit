from typing import Tuple, Sequence

from mkcommit.model import ValidationFailedException, ask
from mkcommit.blocks import Keyword
from mkcommit.validators import matches
from mkcommit.editor_handler import editor

type_keywords = [
    Keyword("feat", "A new feature"),
    Keyword("fix", "A bug fix"),
    Keyword("docs", "Documentation only changes"),
    Keyword("style", "Changes that do not affect the meaning of the code"),
    Keyword("refactor", "A code change that neither fixes a bug nor adds a feature"),
    Keyword("perf", "A code change that improves performance"),
    Keyword("test", "Adding missing tests or correcting existing tests"),
    Keyword("build", "Changes that affect the build system or external dependencies"),
    Keyword("ci", "Changes to our CI configuration files and scripts"),
    Keyword("chore", "Other changes that don't modify src or test files"),
    Keyword("revert", "Reverts a previous commit"),
]


def is_conventional(s: str, allow_default_merge_msg: bool = True) -> bool:
    types = "(" + "|".join([k.keyword for k in type_keywords]) + ")"
    scope = r"(\(.+\))?"
    breaking = r"!?"
    subject = r".+"
    if allow_default_merge_msg:
        merge_msg = "Merge branch.*|"
    else:
        merge_msg = ""

    expression = f"{merge_msg}{types}{scope}{breaking}: {subject}"
    if not matches(expression)(s):
        raise ValidationFailedException(
            "The message is not a valid Conventional Commit"
        )
    return True


def is_word(s: str) -> bool:
    if not matches(r"\S+"):
        raise ValidationFailedException("The scope should be a single word")
    return True


def is_sentence(s: str) -> bool:
    if len(s) < 1:
        raise ValidationFailedException("The message should contain at least one word")
    return True


ask_type = lambda: ask(
    "Select the type of change that you're committing",
    one_of=type_keywords
)

ask_scope = lambda: ask(
    "What is the scope of this change (Optional)",
    check=is_word
)

ask_subject = lambda: ask(
    "Write a short, imperative tense description of the change",
    check=is_sentence
)

ask_body = lambda: ask(
    "Provide a longer description of the change (Optional)",
)

ask_breaking = lambda: ask(
    "Is this a breaking change?",
    yes_no=True
)

ask_breaking_message = lambda: ask(
    "What causes the breaking change (Optional)"
)


def find_trailer(lines: Sequence[str]) -> Tuple[int, int]:
    """
    Find the line number of the start and end of the trailer

    >>> find_trailer(["Line 1", "Line 2"])
    (3, 3)
    >>> find_trailer(["# Comment"])
    (2, 2)
    >>> find_trailer(["Line 1", "# Comment", "", "", "", ""])
    (3, 3)
    >>> find_trailer(["Line 1: Content", "Line 2: Content", "# Comment"])
    (4, 4)
    >>> find_trailer(["Line 1", "Line 2", "", "Trailer-token: Value", "# Comment"])
    (3, 5)
    >>> find_trailer(["", "", "Trailer-token: Value", "Trailer-token: Value"])
    (2, 4)
    >>> find_trailer(["", "Trailer-token: Value", "", "", ""])
    (1, 2)
    >>> find_trailer(["Line 1: Content", "Line 2: Content", "", "Trailer-token: Value"])
    (3, 4)
    >>> find_trailer(["Line 1: Content", "Line 2: Content", "", "# Comment", "Trailer-token: Value"])
    (3, 5)
    >>> find_trailer(["Line 1: Content", "Line 2: Content", "", "# Comment", "# Comment", "Trailer-token: Value"])
    (3, 6)
    """
    trailer_lines = 0
    comment_lines = 0
    for index in range(len(lines) - 1, -1, -1):
        line = lines[index]
        if line.startswith("#"):
            comment_lines += 1
            continue
        if line.strip() == "":
            # Blank line
            if trailer_lines != 0:
                return index + 1, index + 1 + trailer_lines + comment_lines
            continue
        token, sep, value = line.partition(":")
        if sep == "":
            # This is a non-trailer, non-blank line
            if trailer_lines != 0:
                return (
                    index + 2 + comment_lines,
                    index + 2 + trailer_lines + comment_lines,
                )
            # The trailer should be inserted at least two lines later
            return index + 2 + comment_lines, index + 2 + comment_lines
        trailer_lines += 1
    return (
        index + 1 + trailer_lines + comment_lines,
        index + 1 + trailer_lines + comment_lines,
    )


def attach_trailer(body: str, trailer: str) -> str:
    r"""
    Attach a trailer to a message body

    >>> attach_trailer("Line 1\nLine 2\n\nTrailer-token: Value\n", "Inserted: Value")
    'Line 1\nLine 2\n\nInserted: Value\nTrailer-token: Value\n'
    >>> attach_trailer("Line 1\n\n\n", "Inserted: Value")
    'Line 1\n\nInserted: Value\n\n'
    >>> attach_trailer("Line 1", "Inserted: Value")
    'Line 1\n\nInserted: Value'
    >>> attach_trailer("", "Inserted: Value")
    '\nInserted: Value'
    >>> attach_trailer("", "")
    '\n'
    """
    lines = body.split("\n")
    start, end = find_trailer(lines)
    while start > len(lines):
        lines.append("")
    lines.insert(start, trailer)
    return "\n".join(lines)


def default_breaking() -> Tuple[str, str]:
    breaking = ask_breaking()
    if not breaking:
        return "", ""
    breaking_message = ask_breaking_message()
    if breaking_message == "":
        return "!", ""
    else:
        return "", f"BREAKING CHANGE: {breaking_message}"


def basic_short() -> str:
    type = ask_type().keyword
    scope = ask_scope()
    subject = ask_subject()
    if scope:
        return f"{type}({scope}): {subject}"
    else:
        return f"{type}: {subject}"


def default_long() -> str:
    switch = ask("Do you wish to add a longer message?", yes_no=True)
    if switch:
        return editor()
    else:
        return ""


def default() -> Tuple[str, str]:
    type = ask_type().keyword
    scope = ask_scope()
    subject = ask_subject()
    breaking_mark, breaking_trailer = default_breaking()
    long = default_long()

    if scope:
        short = f"{type}({scope}){breaking_mark}: {subject}"
    else:
        short = f"{type}{breaking_mark}: {subject}"

    if breaking_trailer:
        long = attach_trailer(long, breaking_trailer)

    return short, long
