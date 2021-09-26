# mkcommit

<img src="static/logo.png" width="150">

`mkcommit` is an extremely simple tool made for commit message generation.

Run `mkcommit` instead of `git commit` and you will be asked questions that keep your commits tidy even when it's 3 AM.

![mkcommit gif](static/mkcommit.gif)

## Why?

### Why would anybody need this? Aren't editors enough?

When working in teams it's hard to enforce proper Git commit message style from everyone. This CLI tool asks you questions to build a commit message that you can configure for yourself and your team with a very simple Python script.

### `commitlint` exists. Why `mkcommit`?

`commitlint` is a great tool. But it has considerable learning curve if you want to leverage its full potential. This tool strives to be the exact opposite: provide bare minimum with almost no overhead for your teammates. All they will need to learn is this one command: `mkcommit`.

`mkcommit` is:

- Easy to install - all you need is Python (at least version 3.6).
- Easy to configure - all you need is basic Python skills or advanced copy-pasting skills.
- Easy to use - all you need is one command to trigger the commit prompt.
- Scalable - it can be as complex as you want it, with full Git Hook integration and complex validation rules or just with a plain default Semantic Commit generation out-of-the-box.
- Pythonic - might suit you better if you're familiar with Python and don't want to venture into the world of JavaScript.

## Installation

If you have Python set up, you're good to go. Run `pip install mkcommit` and you're done.

## Usage

- Run `mkcommit` to generate a Git commit message and commit changes (calls `git commit -m` underneath).
- Run `mkcommit -s` to generate a Git commit message and print it to standard output.
- Run `mkcommit -c` to generate a Git commmit message and copy it to your clipboard.
- Use `mkcommit -x "some commit message"` to validate an existing commit message from the command line or as a Git Hook command (requires `pre_commit(msg)` function to be implemented in the configuration file).

## Configuration

1. At the root of your repository create a Python filed named `my_repo.mkcommit.py`.
2. Compose the script:

    A built-in _semantic commit_ suite can be used:

    ```python
    from mkcommit import CommitMessage, to_stdout
    from mkcommit.suites import semantic

    def commit():
        return CommitMessage(semantic.default_short())

    if __name__ == "__main__":
        to_stdout(commit())
    ```

    If you need to define your own keywords and commit message template, read [Configuration](https://github.com/kjczarne/mkcommit/wiki/Configuration) in our Wiki.

    If you want to learn how to use the hook mode, read [Hooks](https://github.com/kjczarne/mkcommit/wiki/Hooks) in our Wiki.
3. Run `mkcommit`. You can either:
    - Run it as `mkcommit -f /path/to/some.mkcommit.py`
    - Or trigger it in the current working directory. `mkcommit` will search for all `*.mkcommit.py` files and will let you select the one applicable from the list (this way you can have many config files for many diverse scenarios if you so forsee).

### Input validation

Some of the validators we're offering at the moment:

- `mkcommit.validators.is_int` - validates input as integers
- `mkcommit.validators.is_float` - validates input as floating-point numbers
- `mkcommit.validators.max_len` - raises a validation error if maximum length is exceeded
- `mkcommit.validators.matches` - matches an arbitrary regex pattern

Example of usage:

```python
from mkcommit import Keyword, CommitMessage, ask
from mkcommit.validators import is_int, matches

ticket_number = ask("Ticket number", is_int())    # integer ticket number
initials = ask("Initials", matches(r'\w\w\w\w'))  # 4-letter initials
```

You can learn more about validators in our [Wiki](https://github.com/kjczarne/mkcommit.wiki.git)
