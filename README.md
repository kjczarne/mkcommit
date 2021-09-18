# mkcommit

`mkcommit` is an extremely simple tool made for commit message generation.

## Why?

### Why would anybody need this? Aren't editors enough?

When working in teams it's hard to enforce proper Git commit message style from everyone. This CLI tool asks you questions to build a commit message that you can configure for yourself and your team with a very simple Python script.

### `commitlint` exists. Why `mkcommit`?

`commitlint` is a great tool. But it has considerable learning curve if you want to leverage its full potential. This tool strives to be the exact opposite: provide bare minimum with almost no overhead for your teammates. All they will need to learn is this one command: `mkcommit`.

## Installation

If you have Python set up, you're good to go. Run `pip install mkcommit` and you're done.

## Usage

- Run `mkcommit` to generate a Git commit message and print it to standard output.
- Run `mkcommit -c` to generate a Git commmit message and copy it to your clipboard.

## Configuration

1. At the root of your repository create a Python filed named `my_repo.mkcommit.py`.
2. Compose the script:

    ```python
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

    keyword = ask("Keyword", one_of=keywords)
    ticket_number = ask("Ticket number")
    first_line = ask("Short commit message")
    extended_message = ask("Long commit message")

    c = CommitMessage(
        f"[{ticket_number}] {keyword.keyword}: {first_line}",
        extended_message
    )

    if __name__ == "__main__":
        to_stdout(c)
    ```

    The above example shows a treasure-trove of configuration options:
    - `Keyword` - can be used to create selection lists of keywords
    - `ask` - the main prompt function using `InquirerPy` at the back-end. It consists of the following modes:
      - Bare - e.g. `ask("blah")` asks for direct textual input.
      - `one_of` - asks the user to select one value from a list.
      - `one_or_more` - asks the user to select at least one value from a list.
      - `yes_no` - asks the user a yes/no question.
    - `CommitMessage` - consists of two fields, the first one is the first-line commit message that will appear directly in `git log` and the second field is an extended commit message (usually optional).
    - `to_stdout(c)` at the very end specifies the default behavior when the script is ran directly instead of with `mkcommit`. This is optional if you only intend to use the `mkcommit` command and do not wish to ever trigger the script directly.
3. Run `mkcommit`. You can either:
    - Run it as `mkcommit -f /path/to/some.mkcommit.py`
    - Or trigger it in the current working directory. `mkcommit` will search for all `*.mkcommit.py` files and will let you select the one applicable from the list (this way you can have many config files for many diverse scenarios if you so forsee).
