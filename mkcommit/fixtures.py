from mkcommit.model import Keyword
from typing import List, Any, Optional


def _ask(
    question: str,
    one_of: Optional[List[Any]] = None,
    one_or_more: Optional[List[Any]] = None,
    yes_no: bool = False
):
    answers = {
        "Keyword": Keyword("feat", "Feature"),
        "Your initials": "KrCz",
        "Ticket number": "1234",
        "Short commit message": "cool",
        "Long commit message": ""
    }
    return answers[question]