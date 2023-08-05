import os
import json
from collections import namedtuple
from typing import List, Tuple

import appdirs

from solitude import TOOL_AUTHOR, TOOL_NAME


def get_existing_filepath(
    filename: str, valid_dirs: List[str], allow_non_existing: bool = False
) -> str:
    assert len(valid_dirs) > 0
    full_path = None
    for valid_dir in valid_dirs:
        full_path = os.path.join(valid_dir, filename)
        if os.path.exists(full_path):
            return full_path
    if allow_non_existing:
        return full_path
    raise FileNotFoundError(
        f"Could not find a `{filename}` file in: {valid_dirs}"
    )


def resolve_core_filepaths(
    allow_non_existing: bool = False,
) -> Tuple[str, str, str]:
    # Look for configuration and cache file:
    # 1) locally
    # 2) User home dir `user_config_dir` or `user_cache_dir`
    local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dirs = appdirs.AppDirs(appname=TOOL_NAME, appauthor=TOOL_AUTHOR)
    cache_fname = get_existing_filepath(
        "cache.json",
        valid_dirs=[local_dir, dirs.user_cache_dir],
        allow_non_existing=True,
    )
    config_filepath = get_existing_filepath(
        "config.json",
        valid_dirs=[local_dir, dirs.user_config_dir],
        allow_non_existing=allow_non_existing,
    )
    return cache_fname, config_filepath, local_dir


class Config(object):

    Defaults = namedtuple(
        "defaults", ["username", "priority", "workers", "cmdfiles"]
    )
    SSHConfig = namedtuple("ssh", ["server", "username", "password"])

    class __Config(object):
        def __init__(self):
            self.plugins = []
            self.defaults = Config.Defaults(
                username="UNKNOWN", priority="low", workers=8, cmdfiles=()
            )
            self.ssh = None
            self.cache_path = None
            self.config_path = None
            self.cache_path, self.config_path, _ = resolve_core_filepaths(
                allow_non_existing=True
            )
            self.load_config()

        def is_config_present(self) -> bool:
            return os.path.exists(self.config_path)

        def is_ssh_configured(self) -> bool:
            return self.ssh is not None

        def load_config(self):
            if self.is_config_present():
                with open(self.config_path, "r") as f:
                    cfg = json.load(f)

                if "defaults" in cfg:
                    defaults = cfg["defaults"]
                    # TODO validate defaults

                    self.defaults = Config.Defaults(
                        username="UNKNOWN"
                        if "username" not in defaults
                        else defaults["username"],
                        priority="low"
                        if "priority" not in defaults
                        else defaults["priority"],
                        workers=8
                        if "workers" not in defaults
                        else defaults["workers"],
                        cmdfiles=()
                        if "cmdfiles" not in defaults
                        else tuple(defaults["cmdfiles"]),
                    )
                else:
                    self.defaults = Config.Defaults(
                        username="UNKNOWN", priority="low", workers=8
                    )

                if "ssh" in cfg and all(
                    [
                        e in cfg["ssh"]
                        for e in ["server", "username", "password"]
                    ]
                ):
                    ssh = cfg["ssh"]
                    self.ssh = Config.SSHConfig(
                        server=ssh["server"],
                        username=ssh["username"],
                        password=ssh["password"],
                    )
                else:
                    self.ssh = None

                if (
                    "plugins" in cfg
                    and isinstance(cfg["plugins"], (list, tuple))
                    and all([isinstance(e, str) for e in cfg["plugins"]])
                ):
                    self.plugins = cfg["plugins"]
                else:
                    self.plugins = []

    __instance = None

    def __new__(self):
        if Config.__instance is None:
            Config.__instance = Config.__Config()
        return Config.__instance
