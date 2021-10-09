from mkcommit.module_utils import check_commit_msg_exists, get_commit_msg_from_module, get_commit_msg_func_from_module, get_on_commit_func_from_module, load_module
from mkcommit.model import CommitFunc, CommitMessage, NoFilesFoundException, OnCommitFunc
from typing import Any, Dict, List, Optional, Tuple
import requests
import os
import sys
import shutil
import logging
import yaml
import hashlib
import binascii
import inspect


DEFAULT_TEMP_PATH: str = ".mkcommit-cache"
logger = logging.getLogger(__name__)


def _create_cache(path: str = DEFAULT_TEMP_PATH) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def _recreate_cache(path: str = DEFAULT_TEMP_PATH) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    _create_cache(path)


def _get_configs_map(temp_path: str = DEFAULT_TEMP_PATH) -> Dict[str, str]:
    configs_map_path = os.path.join(temp_path, "configs.yaml")
    configs_map: Dict[str, str] = {}
    if os.path.exists(configs_map_path):
        with open(configs_map_path, "r") as f:
            configs_map = yaml.full_load(f)
    return configs_map
        

def _add_to_configs_map(
    source_url: str,
    target_temp_file_name: str,
    temp_path: str = DEFAULT_TEMP_PATH
) -> None:
    configs_map_path = os.path.join(temp_path, "configs.yaml")
    configs_map: Dict[str, str] = _get_configs_map(temp_path)
    configs_map[source_url] = target_temp_file_name
    with open(configs_map_path, "w") as f:
        yaml.dump(configs_map, f)


def _get_mkcommit_config_from_url(
    url: str,
    target_temp_file_name: str,
    temp_path: str = DEFAULT_TEMP_PATH,
) -> str:
    # first try and load the cached config:
    configs_map = _get_configs_map()
    try:
        target_file_path = os.path.join(temp_path, configs_map[url])
    except KeyError:
        # if there is none, get one from remote:
        response = requests.get(url)
        logger.debug(f"Return code from {url} was {response.status_code}")
        response.raise_for_status()
        
        target_file_path = os.path.join(temp_path, target_temp_file_name)
        
        logger.debug(f"Attempting to write the file to {target_file_path}")
        with open(target_file_path, "w") as f:
            f.write(response.text)
        
        logger.debug(f"Successfully written {url} to {target_file_path}")
        
        logger.debug(f"Attempting to add {url} config to configs.yaml")
        
        _add_to_configs_map(url, target_temp_file_name)
        
        logger.debug(f"{url} config successfully added to configs.yaml")
    
    return target_file_path


def include(
    url: str,
    target_temp_file_name: Optional[str] = None
) -> Tuple[CommitFunc, Optional[OnCommitFunc]]:

    _create_cache()

    if target_temp_file_name:
        inferred_temp_file_name = target_temp_file_name
    else:
        hash_encoder = hashlib.sha256()
        hash_encoder.update(str.encode(url))
        url_hash = hash_encoder.digest()
        inferred_temp_file_name = binascii.hexlify(url_hash).decode("UTF-8")
        inferred_temp_file_name += ".py"

    target_path = _get_mkcommit_config_from_url(url, inferred_temp_file_name)

    load_module(target_path)

    commit_func_or_none = get_commit_msg_func_from_module()

    if commit_func_or_none is None:
        raise NoFilesFoundException(
            f"{url} seems to yield a file that doesn't have a `commit` funciton declaration. "
            "Include functionality is only supported for files that have at least "
            "a `def commit()` whereas `def on_commit()` is optional. "
            "Make sure the file is a valid `mkcommit` configuration file."
        )

    commit_func: CommitFunc = commit_func_or_none

    on_commit_func = get_on_commit_func_from_module()

    return (commit_func, on_commit_func)
