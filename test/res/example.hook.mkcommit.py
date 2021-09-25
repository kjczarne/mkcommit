from dataclasses import dataclass
from re import T
import sys
from typing import Callable, TypeVar, Union
from mkcommit.model import InvalidStateException, ValidationFailedException, Validator, Rule
from mkcommit import CommitMessage, to_stdout, ask
from mkcommit.suites import semantic
from mkcommit.validators import matches, validate_initials
from mkcommit.blocks import Text, Initials


@dataclass
class Rules:
    initials: Rule[Initials] = lambda x: Initials(x, 2, 2)
    something: Rule[Text] = lambda x: Text(x)


def commit() -> CommitMessage:
    initials = ask("Your initials: ")
    Rules.initials(initials).check()
    something = ask("Your something: ")
    Rules.something(something).check(r"blah")
    return CommitMessage(
        f"{initials} | {something}"
    )


def pre_commit(commit_message: CommitMessage):
    rules = Rules()
    initials, something = commit_message.first_line.split(" | ")
    initials_comply = rules.initials(initials).check()
    something_complies = rules.something(something).check(r"blah")

    if not initials_comply:
        raise ValidationFailedException("initials")
    if not something_complies:
        raise ValidationFailedException("something")


if __name__ == "__main__":
    to_stdout(commit())
