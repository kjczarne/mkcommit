from __future__ import annotations
from typing import List
from mkcommit.model import CommaSeparatedList, ValidationFailedException, ask
from mkcommit.blocks import Project
from mkcommit.model import Author as BaseAuthor
from mkcommit.validators import is_int, matches, validate_initials
from mkcommit.suites import semantic
from enum import Enum, auto


class Order(Enum):
    TICKET_FIRST = auto()
    INITIALS_FIRST = auto()


class Author(BaseAuthor):
    def make_initials(self, first_name_chars: int, last_name_chars: int) -> str:
        """Opinionated initials producer compliant with `validate_initials(2,2)`"""
        l_split = self.name.split(" ")
        fname, lname = l_split[0], l_split[-1]
        return fname[0:first_name_chars] + lname[0:last_name_chars]

    @classmethod
    def from_git(cls) -> Author:
        author = super().from_git()
        return cls(author.name, author.email)


def initials_are_2_chars_each(s: str) -> bool:
    """Validates if first name and last name initials have both 2 letters, e.g. 'AbCd'."""
    return validate_initials(2, 2)(s)


def ticket_id_correctly_formatted(s: str) -> bool:
    """Checks if Ticket ID is in the form of 'PROJECTNAME-1234'"""
    return matches(r"^\w+-\d+$|^---$|^-$")(s)


def is_technica(s: str, ticket_first: bool = False) -> bool:
    two_parts = s.split("]")
    if len(two_parts) < 2:
        raise ValidationFailedException(
            f"{s} could not be split on ']' character. "
            "The commit message seems malformed!"
        )
    else:
        preamble = two_parts[0].strip()
        semantic_part = two_parts[1].strip()

        # split the preamble:
        preamble_split = preamble.split("/")
        if len(preamble_split) < 2:
            raise ValidationFailedException(
                "The preamble {preamble}] could not be split on '/' character. "
                "The commit message seems malformed!"
            )
        else:
            # validate the preamble:
            if ticket_first:
                ticket = preamble_split[0].replace("[", "")
                initials = preamble_split[1]
            else:
                initials = preamble_split[0].replace("[", "")
                ticket = preamble_split[1]

        # validate the semantic part:
        if not semantic.is_semantic(semantic_part):
            raise ValidationFailedException(
                "The semantic part of the message, i.e. <keyword>: <message> is "
                f"not compliant with the semantic commit specification. Input was: {semantic_part}"
            )
        else:
            if not initials_are_2_chars_each(initials):
                raise ValidationFailedException(
                    f"Initials should look like AbCd but were {initials}"
                )
            if not ticket_id_correctly_formatted(ticket):
                raise ValidationFailedException(
                    f"Ticket ID should look like PROJECTNAME-1234 but was {ticket}"
                )
            return True


ask_initials = lambda: ask(
    "Your initials (2 letters of your first name + 2 letters of your last name): ",
    check=validate_initials(2, 2)
)
ask_include_ticket = lambda: ask("Is the change linked to an existing ticket?", yes_no=True)
ask_ticket = lambda: ask("Ticket number: ", check=is_int())
ask_order = lambda: ask("Select order: ", list(Order))
ask_short_commit_msg = semantic.ask_short_commit_msg
ask_long_commit_msg = semantic.ask_long_commit_msg
ask_breaking = semantic.ask_breaking


def ask_project(projects: List[Project]) -> str:
    return ask("Select project ID: ", one_of=projects)


def default_short(
    project: Project,
    ticket_first: bool = False,
    initials_from_git: bool = True
) -> str:
    if initials_from_git:
        initials = Author.from_git().make_initials(2, 2)
    else:
        initials = ask_initials()
    is_related_to_ticket = ask_include_ticket()
    if is_related_to_ticket:
        ticket_number = ask_ticket()
        ticket = f"{project.ticket_system_id}-{ticket_number}"
    else:
        ticket = "-"
    keywords = CommaSeparatedList(*[k.keyword for k in semantic.ask_keywords()])
    short_commit = ask_short_commit_msg()
    breaking = "!" if ask_breaking() else ""

    if ticket_first:
        return f"[{ticket}/{initials}] " + \
            f"{keywords}{breaking}: {short_commit}"
    else:
        return f"[{initials}/{ticket}] " + \
            f"{keywords}{breaking}: {short_commit}"


default_long = semantic.default_long
