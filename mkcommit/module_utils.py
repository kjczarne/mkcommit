import importlib.util
import inspect
import sys
from typing import Optional

from mkcommit.model import (
    PRE_COMMIT_FUNC_NAME, CommitFunc, CommitMessage, FailedToFindCommitMessageException,
    ModuleLoaderException, COMMIT_FUNC_NAME, MODULE_SHIM, OnCommitFunc
)


def load_module(file: str):
    """Loads module from filepath using `importlib`

    Args:
        file (str): path to a Python file, intended to use with `.mkcommit.py` files

    Raises:
        ModuleLoaderException: if the loader didn't instantiate for module spec
        ModuleLoaderException: if the module cannot be loaded for any other reason
    """
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


def get_commit_msg_func_from_module() -> Optional[CommitFunc]:
    for _, obj in inspect.getmembers(sys.modules[MODULE_SHIM]):
        if inspect.isfunction(obj) and obj.__name__ == COMMIT_FUNC_NAME:
            return obj


def get_commit_msg_from_module() -> Optional[CommitMessage]:
    """Inspects the module and finds the `CommitMessage` instance

    Returns:
        CommitMessage: the `CommitMessage` object
    """
    commit_message_instance: Optional[CommitMessage] = None
    for _, obj in inspect.getmembers(sys.modules[MODULE_SHIM]):
        if isinstance(obj, CommitMessage):
            commit_message_instance = obj
        elif inspect.isfunction(obj) and obj.__name__ == COMMIT_FUNC_NAME:
            commit_message_instance = obj()
    return commit_message_instance


def check_commit_msg_exists(
    commit_message_instance: Optional[CommitMessage],
    file_path_for_debug: str
) -> CommitMessage:
    """Checks if the provided arg is `CommitMessage` or `None`

    Args:
        commit_message_instance (Optional[CommitMessage]): `CommitMessage` or `None`
        file_path_for_debug (str): file path from where the item was loaded,
            used only to provide meaningful error message

    Raises:
        FailedToFindCommitMessageException: when the provided arg was `None`

    Returns:
        CommitMessage: `CommitMessage` instance when it exists
    """
    if commit_message_instance is None:
        raise FailedToFindCommitMessageException(
            f"Module {file_path_for_debug} seems to not declare any instance "
            "of a `CommitMessage` class. Did you forget to instantiate?"
        )
    else:
        return commit_message_instance


def get_on_commit_func_from_module() -> Optional[OnCommitFunc]:
    module = sys.modules[MODULE_SHIM]
    for _, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__name__ == PRE_COMMIT_FUNC_NAME:
            return obj
