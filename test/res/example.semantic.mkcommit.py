from mkcommit import CommitMessage, to_stdout
from mkcommit.suites import semantic


def commit():
    return CommitMessage(semantic.default_short())


def pre_commit(msg: CommitMessage):
    semantic.is_semantic(msg.first_line)
    semantic.has_short_commit_msg_proper_length(msg.first_line)


if __name__ == "__main__":
    to_stdout(commit())
