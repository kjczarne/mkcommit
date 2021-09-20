from mkcommit import CommitMessage, CommaSeparatedList, Keyword, to_stdout, ask

keywords = [
    Keyword("feat", "New feature"),
    Keyword("fix", "Bug fix")
]

selected_keywords = ask("Select keywords", one_or_more=keywords)
selected_keywords_str = CommaSeparatedList(*[k.keyword for k in selected_keywords])
short_commit_message = ask("Short commit message")

c = CommitMessage(
    f"{selected_keywords_str}: {short_commit_message}"
)

if __name__ == "__main__":
    to_stdout(c)
