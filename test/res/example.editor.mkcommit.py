from mkcommit import CommitMessage, vscode, to_stdout

c = CommitMessage("whatever", vscode())

if __name__ == "__main__":
    to_stdout(c)
