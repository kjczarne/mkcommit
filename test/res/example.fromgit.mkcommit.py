from mkcommit import CommitMessage, to_stdout, Author
from mkcommit.suites import semantic

author = Author.from_git()

c = CommitMessage(
    f"{author.name} | {semantic.default_short()}"
)


if __name__ == "__main__":
    to_stdout(c)
