from mkcommit import CommitMessage, to_stdout
from mkcommit.suites import semantic


c = CommitMessage(semantic.default_short())


if __name__ == "__main__":
    to_stdout(c)
