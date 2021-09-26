from mkcommit import CommitMessage, editor, to_stdout


def commit():
    return CommitMessage("whatever", editor())


if __name__ == "__main__":
    to_stdout(commit())
