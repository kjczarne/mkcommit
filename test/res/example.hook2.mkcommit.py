from dataclasses import dataclass
from mkcommit.model import ValidationFailedException, Rule
from mkcommit import CommitMessage, to_stdout, ask
from mkcommit.blocks import Text, Initials


def two_letter_initials(s: str) -> Initials:
    return Initials(s, 2, 2)


def text_matches(s: str) -> Text:
    return Text(s)


@dataclass
class Rules:
    initials: Rule[Initials] = two_letter_initials
    something: Rule[Text] = text_matches


def commit() -> CommitMessage:
    initials = ask("Your initials: ")
    Rules.initials(initials).check()
    something = ask("Your something: ")
    Rules.something(something).check(r"blah")
    return CommitMessage(
        f"{initials} | {something}"
    )


def on_commit(commit_message: CommitMessage):
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
