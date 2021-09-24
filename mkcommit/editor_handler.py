import os
from platform import platform
from typing import Optional
from mkcommit.model import PlatformUnsupportedException, NotAGitRepoException
from mkcommit.model import _git_command
import subprocess


def _handle_editor(editor_command: Optional[str], file_path: str) -> None:
    if editor_command is None:
        editor_from_git = _git_command("git", "config", "--get", "core.editor")
        if editor_from_git:
            command = f"{editor_from_git} {file_path}"
        else:
            if platform() == "Darwin" or "Linux":
                editor_path = os.environ.get("EDITOR")
                command = f"{editor_path} {file_path}"
            elif platform() == "Windows":
                # TODO: not tested yet on Windows
                command = file_path
            else:
                raise PlatformUnsupportedException(
                    "Supported platforms are macOS, Windows, Linux"
                )
    else:
        command = editor_command
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()


def _init_buffer_file() -> str:
    """Returns file path to the temporary buffer file. Creates the
    temp directory and temp buffer file.
    """
    if not os.path.exists(".git"):
        raise NotAGitRepoException(f"No .git folder found. {os.getcwd()} is not a git repo!")
    file_path = os.path.join(".git", "MKCOMMIT_BUFFER")
    open(file_path, "w").close()
    return file_path


def editor(editor_command: Optional[str] = None) -> str:
    file_path = _init_buffer_file()
    _handle_editor(editor_command, file_path)
    with open(file_path, "r") as f:
        return f.read()


def vscode() -> str:
    file_path = _init_buffer_file()
    return editor(f"code {file_path} --wait")
