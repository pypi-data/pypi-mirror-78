# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Generator, Tuple
from .repo.loader import load_all_installed
from .pybuild import Pybuild, InstallDir, File


def get_installed_files(
    file_type: str,
) -> Generator[Tuple[Pybuild, InstallDir, File], None, None]:
    """Returns a generator over all files of a given type that are currently installed"""
    # FIXME: Deprecated. Remove before 2.0 Instead use load_all_installed and mod.get_files(file_type)
    for mod in load_all_installed(flat=True):
        for install, file in mod.get_files(file_type):
            yield mod, install, file
