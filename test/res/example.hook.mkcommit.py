from mkcommit import CommitMessage, to_stdout, ask, ValidationFailedException
from mkcommit.validators import validate_initials, matches


def initials_are_two_letter(s: str) -> bool:
    if not validate_initials(2, 2)(s):
        raise ValidationFailedException("initials")
    else:
        return True


def something_matches_blah(s: str) -> bool:
    if not matches(r"blah")(s):
        raise ValidationFailedException("something")
    else:
        return True


def commit() -> CommitMessage:
    initials = ask("Your initials: ", check=initials_are_two_letter)
    something = ask("Your something: ", check=something_matches_blah)
    return CommitMessage(
        f"{initials} | {something}"
    )


def on_commit(commit_message: CommitMessage):
    initials, something = commit_message.first_line.split(" | ")
    initials_are_two_letter(initials)
    something_matches_blah(something)


if __name__ == "__main__":
    to_stdout(commit())
