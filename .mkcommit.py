from mkcommit import CommitMessage, to_stdout, ask
from mkcommit.suites import semantic
from mkcommit.validators import is_true

ask("Have you documented your changes?", yes_no=True, check=is_true())
ask("Have you updated the validators list?", yes_no=True, check=is_true())
ask("Have you checked whether the tests are passing?", yes_no=True, check=is_true())


c = CommitMessage(semantic.default_short())


if __name__ == "__main__":
    to_stdout(c)
