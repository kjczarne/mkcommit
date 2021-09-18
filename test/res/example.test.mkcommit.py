from mkcommit import Keyword, CommitMessage, to_stdout
from mkcommit.fixtures import _ask

keywords = [
    Keyword(
        "feat",
        "New feature"
    ),
    Keyword(
        "fix",
        "Bugfix"
    ),
]

ticket_preamble = "MYPROJECT"
keyword = _ask("Keyword", one_of=keywords)
initials = _ask("Your initials")
ticket_number = _ask("Ticket number")
first_line = _ask("Short commit message")
extended_message = _ask("Long commit message")

C = CommitMessage(
    f"[{ticket_preamble}-{ticket_number}/{initials}] {keyword.keyword}: {first_line}",
    extended_message
)

if __name__ == "__main__":
    to_stdout(C)
