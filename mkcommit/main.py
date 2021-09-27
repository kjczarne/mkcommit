import argparse
import glob
import os
from typing import Callable, Optional, Union
import warnings
from enum import Enum
import importlib.util
import inspect
import sys
import pyperclip
import subprocess

from mkcommit.model import (
    CommitMessage, FailedToFindCommitMessageException, ModuleLoaderException,
    WrongModeException, NoFilesFoundException, select, confirm,
    COMMIT_FUNC_NAME, PRE_COMMIT_FUNC_NAME, MODULE_SHIM
)


class Mode(Enum):
    STDOUT = "stdout"
    CLIPBOARD = "clipboard"
    BOTH = "both"
    RUN = "run"
    HOOK = "hook"


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


def to_cmd(msg: Union[str, CommitMessage]):
    if type(msg) is CommitMessage:
        msg_str = msg.make()
    elif type(msg) is str:
        msg_str: str = msg
    else:
        raise TypeError(
            f"Commit message should be `str` or `CommitMessage`, was {type(msg)}"
        )
    yes = confirm(f"The commit message is:\n{msg_str}\n Confirm?")
    if yes:
        subprocess.call(("git", "commit", "-m", msg_str))
    else:
        print("Canceling.")


def to_hook(msg: Union[str, CommitMessage]):
    module = sys.modules[MODULE_SHIM]
    if type(msg) is str:
        raise TypeError(
            f"Whatever is fed to {PRE_COMMIT_FUNC_NAME} should be "
            f"a `CommitMessage` instance ({module.__file__}). This is likely a bug."
        )
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__name__ == PRE_COMMIT_FUNC_NAME:
            obj(msg)
            return  # return `None` after running the hook
    else:
        warnings.warn(f"No hook implemented for template {module.__file__}")


def _main(  # noqa: C901
    file: str,
    mode: Mode,
    commit_msg_str_from_hook: Optional[str] = None,
    to_stdout: Callable[[Union[str, CommitMessage]], None] = to_stdout,
    to_clipboard: Callable[[Union[str, CommitMessage]], None] = to_clipboard,
    to_cmd: Callable[[Union[str, CommitMessage]], None] = to_cmd,
    to_hook: Callable[[Union[str, CommitMessage]], None] = to_hook
):
    def _load_module(file: str):
        spec = importlib.util.spec_from_file_location(
            MODULE_SHIM,
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
            sys.modules[MODULE_SHIM] = cfg_module
        else:
            raise ModuleLoaderException(f"Could not load module located at {file}")

    def _get_commit_msg_from_module():
        commit_message_instance: Optional[CommitMessage] = None
        for name, obj in inspect.getmembers(sys.modules[MODULE_SHIM]):
            if isinstance(obj, CommitMessage):
                commit_message_instance = obj
            elif inspect.isfunction(obj) and obj.__name__ == COMMIT_FUNC_NAME:
                commit_message_instance = obj()
        return commit_message_instance

    def _check_commit_msg_exists(commit_message_instance: Optional[CommitMessage]) -> CommitMessage:
        if commit_message_instance is None:
            raise FailedToFindCommitMessageException(
                f"Module {file} seems to not declare any instance "
                "of a `CommitMessage` class. Did you forget to instantiate?"
            )
        else:
            return commit_message_instance

    _load_module(file)

    if mode == mode.HOOK:
        # in hook mode we check the message fed in as a command line argument
        if commit_msg_str_from_hook is None:
            raise ValueError("Commit message was empty!")
        else:
            lines = commit_msg_str_from_hook.splitlines()
            first_line = lines[0]
            if len(lines) > 1:
                body: str = "\n".join(lines[1:])
            else:
                body: str = ""
            commit_message_instance = CommitMessage(first_line, body)
            to_hook(commit_message_instance)
    elif mode == mode.STDOUT:
        commit_message_instance = _get_commit_msg_from_module()
        to_stdout(_check_commit_msg_exists(commit_message_instance))
    elif mode == mode.CLIPBOARD:
        commit_message_instance = _get_commit_msg_from_module()
        to_clipboard(_check_commit_msg_exists(commit_message_instance))
    elif mode == mode.BOTH:
        commit_message_instance = _get_commit_msg_from_module()
        m = _check_commit_msg_exists(commit_message_instance)
        to_stdout(m)
        to_clipboard(m)
    elif mode == mode.RUN:
        commit_message_instance = _get_commit_msg_from_module()
        to_cmd(_check_commit_msg_exists(commit_message_instance))
    else:
        raise WrongModeException(f"You've used invalid mode: {mode}")


def main():  # noqa: C901
    parser = argparse.ArgumentParser(
        description="`mkcommit` runs `git commit` with an autogenerated message"
    )

    # subparsers = parser.add_subparsers()
    # parser_mk = subparsers.add_parser("mk", help="Create commit messages from templates")
    # parser_lint = subparsers.add_parser("lint", help="Lint a commit message")
    # parser_config = subparsers.add_parser("config", help="Configure `mkcommit`")

    parser.add_argument('-c', '--clipboard',
                        action='store_true', help="Send message to the clipboard instead of STDOUT")
    parser.add_argument('-f', '--file',
                        type=str, help="Path to the commit config file. Must be a "
                        "Python file with `*.mkcommit.py` extension and declaring an instance of "
                        "`mkcommit.CommitMessage` class."
                        )
    parser.add_argument('-s', '--stdout',
                        action='store_true', help="Executes `git commit -m` with whatever output "
                        "was produced by `mkcommit`"
                        )
    parser.add_argument('-x', '--hook',
                        type=str, help="Runs `mkcommit` solely in hook mode, "
                        "i.e. doesn't generate a commit message but validates the one "
                        "provided on the command line. "
                        "This is intended to be used mainly as an entrypoint for `pre-commit` "
                        "hooks"
                        )
    parser.add_argument('-a', '--autoselect',
                        action="store_true", help="Automatically selects "
                        "the first found `*.mkcommit.py` file")

    args = parser.parse_args()

    if args.clipboard and args.stdout:
        mode = Mode.BOTH
    elif args.clipboard:
        mode = Mode.CLIPBOARD
    elif args.stdout:
        mode = Mode.STDOUT
    else:
        mode = Mode.RUN  # Run is default mode

    # if in hook mode, we should override the whole behavior to a hook,
    # so no `to_stdout` and no `to_clipboard` calls will be heeded:
    if args.hook:
        mode = Mode.HOOK

    def _find_files_and_run(root: str):
        with_root = lambda p: os.path.join(root, p)
        mkcommit_files = glob.glob(with_root("*.mkcommit.py"))
        if os.path.exists(with_root(".mkcommit.py")):
            # add also a dotfile if no prefix is used
            mkcommit_files.append(with_root(".mkcommit.py"))
        if len(mkcommit_files) == 0:
            raise NoFilesFoundException("No `*.mkcommit.py` files found")
        if args.autoselect:
            print(os.getcwd())
            selected_file = mkcommit_files[0]
        else:
            selected_file = select(
                "Select one of the following files I've found", mkcommit_files)
        if type(selected_file) is str:
            _main(selected_file, mode, args.hook)
        else:
            raise TypeError("Result was not a string. This is a bug!")

    if args.file:
        _main(args.file, mode, args.hook)
    else:
        if os.path.exists(".mkcommit"):
            try:
                _find_files_and_run(".mkcommit")
            except NoFilesFoundException:
                raise NoFilesFoundException(
                    "No `*.mkcommit.py` files found. `.mkcommit` directory "
                    "exists in this repository, so only that folder will be "
                    "looked up. Move `*.mkcommit.py` files there."
                )
        else:
            _find_files_and_run(".")


if __name__ == "__main__":
    main()
