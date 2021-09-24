from mkcommit import CommitMessage, editor, to_stdout

c = CommitMessage("whatever", editor())

if __name__ == "__main__":
    to_stdout(c)
