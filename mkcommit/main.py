import argparse
import glob
import os
from typing import Type, Union
from InquirerPy import inquirer

from mkcommit.model import CommitMessage, Keyword, ask, NoFilesFoundException


def to_stdout(msg: Union[str, CommitMessage]):
    if type(msg) is CommitMessage:
        print(msg.make())
    else:
        print(msg)


def to_clipboard(msg: Union[str, CommitMessage]):
    # if type(msg) is CommitMessage:
    #     print(msg.make())
    # else:
    #     print(msg)
    pass


def _main(file: str):
    pass


def main():
    parser = argparse.ArgumentParser(description="mkcommit")
    subparsers = parser.add_subparsers()

    parser_mk = subparsers.add_parser("mk", help="Create commit messages from templates")
    parser_lint = subparsers.add_parser("lint", help="Lint a commit message")
    parser_config = subparsers.add_parser("config", help="Configure `mkcommit`")

    parser_mk.add_argument('-ex', '--example',
        action='store_true', help="Print an example message and quit")
    parser_mk.add_argument('-f', '--file',
        type=str, help="Path to the commit config file")
    
    args = parser.parse_args()
    args_mk = parser_mk.parse_args()

    if args_mk.file:
        _main(args_mk.file)
    else:
        mkcommit_files = glob.glob("*.mkcommit.py")
        if len(mkcommit_files) == 0:
            raise NoFilesFoundException("No `*.mkcommit.py` files found")
        selected_file = inquirer.select("Select one of the following files I've found", mkcommit_files).execute()
        if type(selected_file) is str:
            _main(selected_file)
        else:
            raise TypeError("Result was not a string. This is a bug!")


if __name__ == "__main__":
    main()
