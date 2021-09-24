from __future__ import annotations
import subprocess
from typing import Any, Callable, List, Optional, Tuple
from InquirerPy import inquirer
from dataclasses import dataclass
from prettyprinter import pprint

import platform

if platform.system() == "Windows":
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError


class QuestionConflictException(Exception):
    pass


class NoFilesFoundException(Exception):
    pass


class WrongModeException(Exception):
    pass


class FailedToFindCommitMessageException(Exception):
    pass


class ModuleLoaderException(Exception):
    pass


class ValidationFailedException(Exception):
    pass


class InvalidStateException(Exception):
    pass


class PlatformUnsupportedException(Exception):
    pass


class NotAGitRepoException(Exception):
    pass


def _git_command(*args):
    return subprocess.run(
        " ".join(args),
        check=True,
        shell=True,
        capture_output=True
    ).stdout.decode("utf-8").strip()


@dataclass
class Text:
    text: str


@dataclass
class Keyword:
    keyword: str
    description: str


@dataclass
class Project:
    name: str
    ticket_system_id: str
    description: Optional[str] = ""


@dataclass(init=False)
class CommaSeparatedList:
    
    def __init__(self, *args, no_space: bool=False):
        self.elements: Tuple[Any, ...] = args
        self.no_space: bool = no_space
    
    def __repr__(self) -> str:
        # join with commas and spaces and cut off last two
        if self.no_space:
            return "".join([str(i) + "," for i in self.elements])[:-1]
        else:
            return "".join([str(i) + ", " for i in self.elements])[:-2]
    
    def __str__(self) -> str:
        return self.__repr__()


FirstLine = str
Body = str


@dataclass
class CommitMessage:
    first_line: FirstLine
    body: Body = ""

    def make(self, sep: str = "\n\n") -> str:
        if self.body:
            return self.first_line + sep + self.body
        else:
            return self.first_line


@dataclass
class Author:
    name: str
    email: str

    @classmethod
    def from_git(cls) -> Author:
        name = _git_command("git", "config", "--get", "user.name")
        email = _git_command("git", "config", "--get", "user.email")
        return cls(name, email)


Question = str
Validator = Callable[[str], bool]
ValidatorClosure = Callable[..., Validator]


def select(question: str, one_of: List[Any]):
    inquirer_exec = lambda: inquirer.select(question, one_of).execute()
    if platform.system() == "Windows":
        try:
            return inquirer_exec()
        except NoConsoleScreenBufferError:
            print(question)
            pprint([str(i) + " - " + str(j) for i, j in enumerate(one_of)])
            print("\n")
            return one_of[int(input())]
    else:
        return inquirer_exec()


def checkbox(question: str, one_or_more: List[Any]):
    inquirer_exec = lambda: inquirer.checkbox(question, one_or_more).execute()
    if platform.system() == "Windows":
        try:
            return inquirer_exec()
        except NoConsoleScreenBufferError:
            print(question)
            pprint([str(i) + " - " + str(j) for i, j in enumerate(one_or_more)])
            print("\n")
            indices = input().split(",")
            return [one_or_more[int(i)] for i in indices]
    else:
        return inquirer_exec()


def confirm(question: str):
    inquirer_exec = lambda: inquirer.confirm(question).execute()
    if platform.system() == "Windows":
        try:
            return inquirer_exec()
        except NoConsoleScreenBufferError:
            print(question + " (y/n)")
            resp = input()
            if resp.lower() == "y":
                return True
            elif resp.lower() == "n":
                return False
            else:
                return confirm(question)
    else:
        return inquirer_exec()


def text(question: str):
    inquirer_exec = lambda: inquirer.text(question).execute()
    if platform.system() == "Windows":
        try:
            return inquirer.text(question).execute()
        except NoConsoleScreenBufferError:
            print(question)
            print("\n")
            return input()
    else:
        return inquirer_exec()


def ask(
    question: Question,
    one_of: Optional[List[Any]] = None,
    one_or_more: Optional[List[Any]] = None,
    yes_no: bool = False,
    check: Optional[Validator] = None
) -> Any:

    result = None
    stepped_in_flag = False
    if one_of:
        stepped_in_flag = True
        if one_or_more or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result: Any = select(question, one_of)
    if one_or_more:
        stepped_in_flag = True
        if one_of or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result: Any = checkbox(question, one_or_more)
    if yes_no:
        stepped_in_flag = True
        if one_of or one_or_more:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result: Any = confirm(question)
    if not stepped_in_flag:
        result: Any = text(question)

    # WARNING: do not refactor as `if result`, will fail!!!
    if result is not None:
        if check:
            if check(result):
                return result
            else:
                raise ValidationFailedException(
                    f"Question: {question}, validator: {check.__doc__}"
                )
        else:
            return result
    else:
        raise InvalidStateException(
            "Invalid state on `ask`: "
            f"one_or_more={one_or_more}, one_of={one_of}, yes_no={yes_no}, "
            f"check={check}"
        )
