from typing import Callable, List, Optional, Tuple
from mkcommit.model import ValidationFailedException, ask, CommaSeparatedList
from mkcommit.blocks import Keyword
from mkcommit.validators import matches, max_len
from mkcommit.editor_handler import editor

commit_keywords = [
    Keyword("feat", "A new feature"),
    Keyword("fix", "A bug fix"),
    Keyword("docs", "Documentation only changes"),
    Keyword("style", "Changes that do not affect the meaning of the code"),
    Keyword("refactor", "A code change that neither fixes a bug nor adds a feature"),
    Keyword("wip", "Work in progress (think whether it really should be committed first)"),
    Keyword("test", "Adding missing tests or correcting existing tests"),
    Keyword("chore", "Other changes that don't modify src or test files"),
    Keyword("revert", "Reverts a previous commit"),
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


def _is_semantic_with_custom_keyword_set(
    commit_keywords: List[Keyword],
    allow_keywords_with_commas: bool,
    validation_error_message: str
) -> Callable[[str, bool], bool]:

    def closure(s: str, allow_default_merge_msg: bool = True):
        scope = r"(\([^, ]+\))?"
        breaking = r"!?"

        kwds = "(" + "|".join([
            "(" + k.keyword + scope + breaking + ")"
            for k in commit_keywords]) + ")"

        kwds_with_commas = "(" + "|".join([
            "((" + k.keyword + scope + breaking + ")" + r", ?" + ")"
            for k in commit_keywords]) + ")"

        subject = r"[^,]+"
        if allow_default_merge_msg:
            merge_msg = "Merge branch.*|"
        else:
            merge_msg = ""

        expression = f"^{merge_msg}{kwds}: {subject}"
        if allow_keywords_with_commas:
            expression = f"{expression}|^{merge_msg}{kwds_with_commas}+{kwds}: {subject}"
        if not matches(expression)(s):
            raise ValidationFailedException(
                validation_error_message
            )
        return True

    return closure


def is_semantic(s: str, allow_default_merge_msg: bool = True) -> bool:
    """True if the message corresponds to a Semantic Commit message."""
    return _is_semantic_with_custom_keyword_set(
        commit_keywords,
        allow_keywords_with_commas=True,
        validation_error_message="The message does not comply with "
                                 "semantic commit formatting rules. "
                                 f"Was {s}, but should look like e.g. 'feat: something implemented'"
    )(s, allow_default_merge_msg)


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


def _make_first_line(
    scope: Optional[str]
) -> Callable[[str, str, str], str]:

    def closure(
        keywords: str,
        breaking_mark: str,
        subject: str
    ):
        if scope is not None:
            return f"{keywords}({scope}){breaking_mark}: {subject}"
        else:
            return f"{keywords}{breaking_mark}: {subject}"

    return closure


def default_short() -> str:
    keywords = str(CommaSeparatedList(*[k.keyword for k in ask_keywords()]))
    scope = ask_scope()
    short_commit = ask_short_commit_msg()
    breaking = "!" if ask_breaking() else ""
    return _make_first_line(scope)(keywords, breaking, short_commit)


def default_long() -> str:
    switch = ask("Do you wish to add a longer message?", yes_no=True)
    if switch:
        return editor()
    else:
        return ""


def default() -> Tuple[str, str]:
    return default_short(), default_long()
