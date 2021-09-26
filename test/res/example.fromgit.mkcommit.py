from mkcommit import CommitMessage, to_stdout, Author
from mkcommit.suites import semantic

def commit():
    author = Author.from_git()

    return CommitMessage(
        f"{author.name} | {semantic.default_short()}"
    )


if __name__ == "__main__":
    to_stdout(commit())
