from mkcommit.model import ask, CommaSeparatedList
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
    return s in [k.keyword for k in commit_keywords]


def is_semantic(s: str) -> bool:
    """True if the message corresponds to a Semantic Commit message."""
    kwds = "|".join([k.keyword for k in commit_keywords])
    return matches(kwds + r"(\(.+\))?: .+")(s)


def has_short_commit_msg_proper_length(s: str) -> bool:
    """True if the included raw commit message (after colon) is less than
    55 characters.
    """
    return is_shorter_than_55_chars(s.split(":")[1].strip())


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
