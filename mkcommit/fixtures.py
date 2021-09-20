from mkcommit.model import Keyword, Validator
from typing import List, Any, Optional


def _ask(
    question: str,
    one_of: Optional[List[Any]] = None,
    one_or_more: Optional[List[Any]] = None,
    yes_no: bool = False,
    check: Optional[Validator] = None
) -> Any:
    answers = {
        "Keyword": Keyword("feat", "Feature"),
        "Your initials": "KrCz",
        "Ticket number": "1234",
        "Short commit message": "cool",
        "Long commit message": "",
        "Integer Test": "1234",
        "Float Test": "12.0",
        "Regex Test": "match_me",
        "Max Length Test": "this is shorter than 30 chars",
        "Initials": "KrzCza",
        "Integer Test Invalid": "asdf",
        "Float Test Invalid": "qwer",
        "Regex Test Invalid": "no_match",
        "Max Length Test Invalid": "this is not shorter than 30 chars",
        "Initials Invalid": "KrzyCzar",
        "Initials Invalid2": "KrzCzar",
    }
    result = answers[question]

    if check:
        if check(result):
            return result
        else:
            return f"INVALID-{result}"
    else:
        return result
