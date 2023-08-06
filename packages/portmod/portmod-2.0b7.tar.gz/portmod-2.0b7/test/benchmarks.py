# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import pytest
import shutil
from portmod.globals import env
from portmod.execute import execute
from .env import setup_env, tear_down_env

TMP_REPO = os.path.join(os.path.dirname(env.TMP_DIR), "not-portmod")
TMP_FILE = os.path.join(TMP_REPO, "test", "test.pybuild")
env.ALLOW_LOAD_ERROR = False


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def canimport(name: str) -> bool:
    """Returns true if the given module can be imported"""
    try:
        __import__(name)
        return True
    except ModuleNotFoundError:
        return False


@pytest.mark.skipif(
    not canimport("pytest_benchmark"), reason="requires pytest-benchmark"
)
def test_import_speed(benchmark):
    merge_path = shutil.which("omwmerge")
    command = f"{merge_path} --help"

    benchmark(execute, command)
