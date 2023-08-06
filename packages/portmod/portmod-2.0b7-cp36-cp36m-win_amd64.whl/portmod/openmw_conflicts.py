# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Displays filesystem conflicts between mods
"""

from portmod.portmod import file_conflicts

from .vfs import get_vfs_dirs


def main():
    """
    Main executable for openmw-conflicts executable
    """
    mod_dirs = get_vfs_dirs()

    file_conflicts(mod_dirs, ["txt", "md"])
