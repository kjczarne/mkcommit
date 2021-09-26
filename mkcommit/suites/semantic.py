from mkcommit.model import ValidationFailedException, ask, CommaSeparatedList
from mkcommit.blocks import Keyword
from mkcommit.validators import matches, max_len
from mkcommit.editor_handler import editor

commit_keywords = [
    Keyword("feat", "New Feature"),
    Keyword("fix", "Bug Fix"),
    Keyword("chore", "Generic task"),
    Keyword("wip", "Work in progress"),
    Keyword("doc", "Documentation updated"),
    Keyword("refactor", "Refactoring something"),
    Keyword("test", "Added a test, tested an element"),
    Keyword("revert", "Revert a previous change"),
    Keyword("style", "Improved code style"),
    Keyword("clean", "Cleaned up unnecessary stuff")
]


def is_shorter_than_55_chars(s: str) -> bool:
    """True if the input is shorter than 55 characters."""
    return max_len(55)(s)


def is_keyword(s: str) -> bool:
    """True if the input is a valid Semantic Commit keyword."""
    str_keywords = [k.keyword for k in commit_keywords]
    if s not in str_keywords:
        raise ValidationFailedException(
            f"{s} is not a valid keyword. Should be one of: {str_keywords}"
        )
    else:
        return True


def is_semantic(s: str) -> bool:
    """True if the message corresponds to a Semantic Commit message."""
    kwds = "(" + "|".join([k.keyword for k in commit_keywords]) + ")"
    kwds_with_commas = "(" + "|".join([k.keyword + r", ?" for k in commit_keywords]) + ")"
    # like: r"(feat|fix)(\(.+\))?: .+|(feat, ?|fix, ?)(feat|fix)(\(.+\))?: .+"
    description = r"((\(.+\))?: .+)"
    if not matches(kwds + description + "|" + kwds_with_commas + kwds + description)(s):
        raise ValidationFailedException(
            "The message does not comply with a semantic commit formatting rules. "
            f"Was {s}, but should look like e.g. 'feat: something implemented'"
        )
    else:
        return True


def has_short_commit_msg_proper_length(s: str) -> bool:
    """True if the included raw commit message (after colon) is less than
    55 characters.
    """
    desc = s.split(":")[1].strip()
    if not is_shorter_than_55_chars(desc):
        raise ValidationFailedException(
            "The raw description included in the semantic commit message "
            f"should be shorter than 55 characters, was {len(desc)}"
        )
    return True


ask_keywords = lambda: ask(
    "Select one or more keywords applicable (use TAB): ",
    one_or_more=commit_keywords
)

ask_scope = lambda: ask(
    "(Optional) provide change scope: "
)

ask_short_commit_msg = lambda: ask(
    "Provide the short commit msg, max 55 characters long: ",
    check=is_shorter_than_55_chars
)

ask_long_commit_msg = lambda: ask(
    "Provide the long commit msg: "
)

ask_breaking = lambda: ask(
    "Is this a breaking change?",
    yes_no=True
)


def default_short() -> str:
    keywords = CommaSeparatedList(*[k.keyword for k in ask_keywords()])
    scope = ask_scope()
    short_commit = ask_short_commit_msg()
    breaking = "!" if ask_breaking() else ""
    if scope:
        return f"{keywords}({scope}){breaking}: {short_commit}"
    else:
        return f"{keywords}{breaking}: {short_commit}"


def default_long() -> str:
    return editor()
