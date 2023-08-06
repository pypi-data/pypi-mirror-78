# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
BLACKLIST and WHITELIST tests
"""

import os
import zipfile
import pytest
from portmod.repo.loader import full_load_file
from portmod.globals import env
from portmod.mod import install_mod
from .env import setup_env, tear_down_env
from .test_loader import create_pybuild, TMP_FILE


LISTED = set(
    map(
        os.path.normpath,
        ["directory/foo.txt", "directory/bar.txt", "directory/bar.png"],
    )
)
OTHER = set(map(os.path.normpath, ["foo.txt", "directory/bar.gif"]))


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def create_zip():
    """Creates test zip file"""
    os.chdir(env.TMP_DIR)
    os.makedirs(env.DOWNLOAD_DIR, exist_ok=True)
    with zipfile.ZipFile(os.path.join(env.DOWNLOAD_DIR, "test.zip"), "w") as myzip:
        for file in LISTED | OTHER:
            if os.path.dirname(file):
                os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, "w+") as filep:
                print("", file=filep)
            myzip.write(file, file)


def test_whitelist(setup):
    """
    Tests that InstallDir whitelisting works properly
    """
    pybuild = """
import os
import sys
from pybuild import Pybuild1, InstallDir

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
    SRC_URI="test.zip"

    INSTALL_DIRS=[
        InstallDir(".", WHITELIST=["directory/*.txt", "directory/*.png", "*.jpg"]),
    ]
    """
    create_zip()
    create_pybuild(pybuild)
    mod = full_load_file(TMP_FILE)
    install_mod(mod)

    base = os.path.join(env.MOD_DIR, "test", "test")
    whitelisted = LISTED.copy()
    for root, _, files in os.walk(base):
        for file in files:
            path = os.path.relpath(root, base)
            fullpath = os.path.normpath(os.path.join(path, file))
            if fullpath in whitelisted:
                whitelisted.discard(fullpath)
            else:
                raise Exception(f"File {fullpath} is not in the whitelist!")

    # Only the whitelisted file can be present
    assert not whitelisted


def test_blacklist(setup):
    """
    Tests that InstallDir blacklisting works properly
    """
    pybuild = """
import os
import sys
from pybuild import Pybuild1, InstallDir

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
    SRC_URI="test.zip"

    INSTALL_DIRS=[
        InstallDir(".", BLACKLIST=["directory/*.txt", "directory/*.png", "*.jpg"]),
    ]
    """
    create_zip()
    create_pybuild(pybuild)
    mod = full_load_file(TMP_FILE)
    install_mod(mod)

    other_files = OTHER.copy()

    base = os.path.join(env.MOD_DIR, "test", "test")
    for root, _, files in os.walk(base):
        for file in files:
            path = os.path.relpath(root, base)
            fullpath = os.path.normpath(os.path.join(path, file))
            if fullpath in LISTED:
                raise Exception(f"File {fullpath} is in the black!")
            if fullpath in other_files:
                other_files.discard(fullpath)

    assert not other_files
