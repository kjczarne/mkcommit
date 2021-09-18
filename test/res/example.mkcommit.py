from mkcommit import Keyword, CommitMessage, ask, to_stdout

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
keyword = ask("Keyword", one_of=keywords)
# keyword = ask("Keyword", one_or_more=keywords)
initials = ask("Your initials")
ticket_number = ask("Ticket number")
first_line = ask("Short commit message")
extended_message = ask("Long commit message")

C = CommitMessage(
    f"[{ticket_preamble}-{ticket_number}/{initials}] {keyword.keyword}: {first_line}",
    extended_message
)

if __name__ == "__main__":
    to_stdout(C)
