from mkcommit.model import ValidationFailedException
from mkcommit import CommitMessage, to_stdout
from mkcommit.suites import semantic


def commit():
    return CommitMessage(semantic.default_short())


def pre_commit(msg: CommitMessage):
    if not semantic.is_semantic(msg.first_line):
        raise ValidationFailedException(
            "The commit message is not a valid Semantic Commit message"
        )
    if not semantic.has_short_commit_msg_proper_length(msg.first_line):
        raise ValidationFailedException(
            "The description following the Semantic Commit keyword is "
            "too long. Should be at most 55 characters long."
        )


if __name__ == "__main__":
    to_stdout(commit())
