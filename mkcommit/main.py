import argparse
import glob
import os
from typing import Optional, Type, Union
from InquirerPy import inquirer
from enum import Enum
import importlib.util
import inspect
import sys
import pyperclip

from mkcommit.model import CommitMessage, FailedToFindCommitMessageException, Keyword, ModuleLoaderException, WrongModeException, ask, NoFilesFoundException


class Mode(Enum):
    STDOUT = "stdout"
    CLIPBOARD = "clipboard"


def to_stdout(msg: Union[str, CommitMessage]):
    if type(msg) is CommitMessage:
        print(msg.make())
    else:
        print(msg)


def to_clipboard(msg: Union[str, CommitMessage]):
    if type(msg) is CommitMessage:
        pyperclip.copy(msg.make())
    else:
        pyperclip.copy(msg)


def _main(file: str, mode: Mode):
    commit_message_instance: Optional[CommitMessage] = None
    module_shim = "mkcommit.loaded_config"
    spec = importlib.util.spec_from_file_location(
        module_shim,
        file
    )
    
    if spec:
        cfg_module = importlib.util.module_from_spec(spec)
        if spec.loader:
            getattr(spec.loader, "exec_module")(cfg_module)
        else:
            raise ModuleLoaderException(
                f"Loaded module ({file}) spec does not have a valid loader"
            )
        sys.modules[module_shim] = cfg_module
    else:
        raise ModuleLoaderException(f"Could not load module located at {file}")
    
    for name, obj in inspect.getmembers(sys.modules[module_shim]):
        if isinstance(obj, CommitMessage):
            commit_message_instance = obj
    
    if commit_message_instance is None:
        raise FailedToFindCommitMessageException(
            f"Module {file} seems to not declare any instance "
            "of a `CommitMessage` class. Did you forget to instantiate?"
        )
    else:
        if mode.STDOUT:
            to_stdout(commit_message_instance)
        elif mode.CLIPBOARD:
            to_clipboard(commit_message_instance)
        else:
            raise WrongModeException(f"You've used invalid mode: {mode}")


def main():
    parser = argparse.ArgumentParser(description="mkcommit")
    
    # subparsers = parser.add_subparsers()
    # parser_mk = subparsers.add_parser("mk", help="Create commit messages from templates")
    # parser_lint = subparsers.add_parser("lint", help="Lint a commit message")
    # parser_config = subparsers.add_parser("config", help="Configure `mkcommit`")

    parser.add_argument('-c', '--clipboard',
        action='store_true', help="Send message to the clipboard instead of STDOUT")
    parser.add_argument('-f', '--file',
        type=str, help="Path to the commit config file. Must be a Python file named "
                       "with `*.mkcommit.py` extension and declaring an instance of "
                       "`mkcommit.CommitMessage` class."
    )
    
    args = parser.parse_args()

    if args.clipboard:
        mode = Mode.CLIPBOARD
    else:
        mode = Mode.STDOUT

    if args.file:
        _main(args.file, mode)
    else:
        mkcommit_files = glob.glob("*.mkcommit.py")
        if len(mkcommit_files) == 0:
            raise NoFilesFoundException("No `*.mkcommit.py` files found")
        selected_file = inquirer.select("Select one of the following files I've found", mkcommit_files).execute()
        if type(selected_file) is str:
            _main(selected_file, mode)
        else:
            raise TypeError("Result was not a string. This is a bug!")


if __name__ == "__main__":
    main()
