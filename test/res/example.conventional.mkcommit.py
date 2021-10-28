from mkcommit import CommitMessage, to_stdout
from mkcommit.suites import conventional


def commit():
    first_line, body = conventional.default()
    conventional.is_conventional(first_line)
    return CommitMessage(first_line, body)


def on_commit(msg: CommitMessage):
    conventional.is_conventional(msg.first_line)


if __name__ == "__main__":
    to_stdout(commit())
