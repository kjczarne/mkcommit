from mkcommit import CommitMessage, to_stdout, Project
from mkcommit.suites import technica


project = Project("Some project", "SOMEPROJ")


c = CommitMessage(
    technica.default_short(project, ticket_first=True)
)


if __name__ == "__main__":
    to_stdout(c)
