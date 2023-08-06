# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import logging
import os
import shlex
import subprocess
import sys
from typing import Optional
from contextlib import contextmanager
from .repo.loader import load_all_installed
from .repo.usestr import use_reduce
from .globals import env
from .config import get_config


def execute(
    command: str,
    pipe_output: bool = False,
    pipe_error: bool = False,
    err_on_stderr: bool = False,
    check: bool = True,
) -> Optional[str]:
    """
    Executes the given command

    This function handles any platform-specific behaviour,
    in addition to output redirection and decoding.
    """
    if sys.platform == "win32":
        cmd = command
    else:
        cmd = shlex.split(command)

    output = None
    error = None
    if pipe_output or logging.root.level >= logging.WARN:
        output = subprocess.PIPE
    if err_on_stderr or pipe_error or logging.root.level >= logging.WARN:
        error = subprocess.PIPE
    proc = subprocess.run(cmd, check=check, stdout=output, stderr=error)

    if err_on_stderr and proc.stderr:
        raise subprocess.CalledProcessError(0, cmd, proc.stdout, proc.stderr)

    output = ""
    if pipe_output and proc.stdout:
        output += proc.stdout.decode("utf-8")
    if pipe_error and proc.stderr:
        output += proc.stderr.decode("utf-8")
    if pipe_output or pipe_error:
        return output


@contextmanager
def _pybuild_exec_paths():
    old_path = os.environ["PATH"]
    for mod in load_all_installed(flat=True):
        if "exec" in use_reduce(mod.PROPERTIES, mod.INSTALLED_USE, flat=True):
            bin_path = os.path.join(
                env.MOD_DIR, mod.CATEGORY, mod.MN, get_config()["EXEC_PATH"]
            )
            os.environ["PATH"] += os.pathsep + bin_path
    try:
        yield
    finally:
        os.environ["PATH"] = old_path
