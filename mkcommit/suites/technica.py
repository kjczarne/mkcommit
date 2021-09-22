from typing import List
from mkcommit.model import CommaSeparatedList, ask, Project
from mkcommit.validators import is_int, validate_initials
from mkcommit.suites.semantic import (
    ask_keywords, ask_breaking, ask_short_commit_msg, ask_long_commit_msg,
    default_long
)
from enum import Enum, auto


class Order(Enum):
    TICKET_FIRST = auto()
    INITIALS_FIRST = auto()


ask_initials = lambda: ask(
    "Your initials (2 letters of your first name + 2 letters of your last name): ",
    check=validate_initials(2, 2)
)
ask_ticket = lambda: ask("Ticket number: ", check=is_int())
ask_order = lambda: ask("Select order: ", list(Order))


def ask_project(projects: List[Project]) -> str:
    return ask("Select project ID: ", one_of=projects)


def default_short(project: Project, ticket_first: bool = False) -> str:
    initials = ask_initials()
    ticket = ask_ticket()
    keywords = CommaSeparatedList(*[k.keyword for k in ask_keywords()])
    short_commit = ask_short_commit_msg()
    breaking = "!" if ask_breaking() else ""
    
    if ticket_first:
        return f"[{project.ticket_system_id}-{ticket}/{initials}] " + \
            f"{keywords}{breaking}: {short_commit}"
    else:
        return f"[{initials}/{project.ticket_system_id}-{ticket}] " + \
            f"{keywords}{breaking}: {short_commit}"
