from mkcommit import CommitMessage, to_stdout, ask
from mkcommit.suites import semantic
from mkcommit.validators import is_true


def commit():
    ask("Have you documented your changes?", yes_no=True, check=is_true())
    ask("Have you updated the validators list?", yes_no=True, check=is_true())
    ask("Have you checked whether the tests are passing?", yes_no=True, check=is_true())

    return CommitMessage(semantic.default_short())


def pre_commit(msg: CommitMessage):
    pass  # TODO: semantic doesn't declare a validator yet


if __name__ == "__main__":
    to_stdout(commit())
