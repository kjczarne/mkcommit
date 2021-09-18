from typing import Any, Callable, List, Optional
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


class ValidationFailedException(Exception):
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
Validator = Callable[[str], bool]
ValidatorClosure = Callable[..., Validator]


def ask(
    question: Question,
    one_of: Optional[List[Any]] = None,
    one_or_more: Optional[List[Any]] = None,
    yes_no: bool = False,
    check: Optional[Validator] = None
) -> Any:

    result = None
    if one_of:
        if one_or_more or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result = inquirer.select(question, one_of).execute()
    if one_or_more:
        if one_of or yes_no:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result = inquirer.checkbox(question, one_or_more).execute()
    if yes_no:
        if one_of or one_or_more:
            raise QuestionConflictException(
                "Check your `ask` calls. You should only use one extra arg "
                f"when calling `ask`. The args are: `one_of`:{one_of}, "
                f"`one_or_more`:{one_or_more}, `yes_no`:{yes_no}"
            )
        result = inquirer.confirm(question).execute()
    result = inquirer.text(question).execute()

    if check:
        if check(result):
            return result
        else:
            raise ValidationFailedException(
                f"Question: {question}, validator: {check.__name__}"
            )
    else:
        return result
