from mkcommit.model import ValidationFailedException
from mkcommit import CommitMessage, to_stdout, ask
from mkcommit.validators import validate_initials, matches


def initials_are_two_letter(s: str) -> bool:
    return validate_initials(2, 2)(s)


def something_matches_blah(s: str) -> bool:
    return matches(r"blah")(s)


def commit() -> CommitMessage:
    initials = ask("Your initials: ", check=initials_are_two_letter)
    something = ask("Your something: ", check=something_matches_blah)
    return CommitMessage(
        f"{initials} | {something}"
    )


def pre_commit(commit_message: CommitMessage):
    initials, something = commit_message.first_line.split(" | ")
    initials_comply = initials_are_two_letter(initials)
    something_complies = something_matches_blah(something)

    if not initials_comply:
        raise ValidationFailedException("initials")
    if not something_complies:
        raise ValidationFailedException("something")


if __name__ == "__main__":
    to_stdout(commit())
