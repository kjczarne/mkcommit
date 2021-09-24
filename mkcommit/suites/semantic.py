from mkcommit.model import Keyword, ask, CommaSeparatedList
from mkcommit.validators import max_len
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

ask_keywords = lambda: ask(
    "Select one or more keywords applicable (use TAB): ",
    one_or_more=commit_keywords
)

ask_scope = lambda: ask(
    "(Optional) provide change scope: "
)

ask_short_commit_msg = lambda: ask(
    "Provide the short commit msg, max 55 characters long: ",
    check=max_len(55)
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
