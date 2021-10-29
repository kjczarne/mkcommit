from mkcommit import to_stdout, include

commit, on_commit = include(
    "https://raw.githubusercontent.com/kjczarne/mkcommit/master/test/res/example.semantic.mkcommit.py")  # noqa: E501
commit, on_commit = include(
    "https://raw.githubusercontent.com/kjczarne/mkcommit/master/test/res/example.semantic.mkcommit.py",  # noqa: E501
    "tempname.mkcommit.py"
)


if __name__ == "__main__":
    to_stdout(commit())
