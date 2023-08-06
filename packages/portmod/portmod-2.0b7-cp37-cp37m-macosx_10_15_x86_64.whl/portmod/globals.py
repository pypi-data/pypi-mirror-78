# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import tempfile
from appdirs import AppDirs
from functools import lru_cache


@lru_cache()
def get_version() -> str:
    """Returns portmod version"""
    try:
        from ._version import version

        return version
    except ImportError:
        osp = os.path
        possible_root = osp.dirname(osp.dirname(osp.realpath(__file__)))
        if osp.isfile(osp.join(possible_root, ".portmod_not_installed")):
            # Only a dev dependency and is otherwise unneeded at runtime
            import setuptools_scm

            return setuptools_scm.get_version(possible_root)
        else:
            try:
                from importlib.metadata import version
            except ModuleNotFoundError:
                from importlib_metadata import version

            return version("portmod")


class Env:
    DEBUG = False

    APP_NAME = "portmod"
    DIRS = AppDirs(APP_NAME)

    TMP_DIR = os.path.join(tempfile.gettempdir(), "portmod")

    PORTMOD_CONFIG_DIR = DIRS.user_config_dir
    SET_DIR = os.path.join(PORTMOD_CONFIG_DIR, "sets")
    PORTMOD_CONFIG = os.path.join(PORTMOD_CONFIG_DIR, "portmod.conf")

    PORTMOD_LOCAL_DIR = DIRS.user_data_dir
    MOD_DIR = os.path.join(PORTMOD_LOCAL_DIR, "mods")
    CACHE_DIR = DIRS.user_cache_dir
    DOWNLOAD_DIR = os.path.join(CACHE_DIR, "downloads")
    PYBUILD_CACHE_DIR = os.path.join(CACHE_DIR, "pybuild")
    CONFIG_PROTECT_DIR = os.path.join(CACHE_DIR, "cfg_protect")

    INSTALLED_DB = os.path.join(PORTMOD_LOCAL_DIR, "db")
    PORTMOD_MIRRORS_DEFAULT = "https://gitlab.com/portmod/mirror/raw/master/"

    ALLOW_LOAD_ERROR = True

    REPO = "https://gitlab.com/portmod/openmw-mods.git"
    REPOS_FILE = os.path.join(PORTMOD_CONFIG_DIR, "repos.cfg")

    REPOS = []

    INTERACTIVE = True

    TESTING = False


env = Env()


if not env.REPOS:
    import portmod.repos

    env.REPOS = portmod.repos.get_repos()
