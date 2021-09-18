from typing import Any, List, Optional
from InquirerPy import inquirer
from dataclasses import dataclass


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


@dataclass
class Text:
    text: str


@dataclass
class Keyword:
    keyword: str
    description: str


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


Question = str


def ask(
    question: Question,
    one_of: Optional[List[Any]] = None,
    one_or_more: Optional[List[Any]] = None,
    yes_no: bool = False
):
    
    if one_of:
        if one_or_more or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        return inquirer.select(question, one_of).execute()
    if one_or_more:
        if one_of or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        return inquirer.checkbox(question, one_or_more).execute()
    if yes_no:
        if one_of or one_or_more:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        return inquirer.confirm(question).execute()
    return inquirer.text(question).execute()
