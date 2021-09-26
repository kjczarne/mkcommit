from mkcommit import CommitMessage, to_stdout, Project
from mkcommit.suites import technica


def commit():
    project = Project("Some project", "SOMEPROJ")

    return CommitMessage(
        technica.default_short(project, ticket_first=True)
    )

def on_commit(msg: CommitMessage):
    technica.is_technica(msg.first_line)


if __name__ == "__main__":
    to_stdout(commit())
