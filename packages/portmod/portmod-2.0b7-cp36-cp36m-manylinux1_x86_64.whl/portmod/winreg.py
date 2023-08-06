# a Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

# pylint: disable=no-member

"""
Helper functions for interacting with the Windows registry
"""

import sys

if sys.platform == "win32":
    import os
    import winreg  # pylint: disable=import-error
    from typing import Optional

    def read_reg(key: str, subkey: str, entry: Optional[str] = None):
        """
        Reads the given registry
        """
        with winreg.ConnectRegistry(None, key) as reg:
            try:
                rawkey = winreg.OpenKey(
                    reg, subkey, access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                )
            except FileNotFoundError:
                try:
                    rawkey = winreg.OpenKey(
                        reg, subkey, access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY
                    )
                except FileNotFoundError:
                    return None

            if entry is None:
                subkeys = {}
                i = 0
                try:
                    while True:
                        subsubkey = winreg.EnumKey(rawkey, i)
                        subkeys[subsubkey] = read_reg(
                            key, subkey + os.sep + subsubkey, entry
                        )
                        i += 1
                except WindowsError:  # pylint: disable=undefined-variable
                    if subkeys:
                        return subkeys
            try:
                i = 0
                while True:
                    name, value, _ = winreg.EnumValue(rawkey, i)
                    if entry is None:
                        return value
                    if name == entry:
                        return value
                    i += 1
            except WindowsError:  # pylint: disable=undefined-variable
                return None
