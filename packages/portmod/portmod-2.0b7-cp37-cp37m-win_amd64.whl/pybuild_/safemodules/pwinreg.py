# a Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Helper functions for interacting with the Windows registry
"""

from typing import Optional

import os
import sys
from portmod.io_guard import _check_call, IOType

if sys.platform == "win32":
    from winreg import (  # noqa  # pylint: disable=unused-import,import-error,no-name-in-module
        HKEY_LOCAL_MACHINE,
        HKEY_CLASSES_ROOT,
        HKEY_CURRENT_USER,
        HKEY_USERS,
        HKEY_CURRENT_CONFIG,
    )

    from portmod.winreg import read_reg as _read_reg

    def read_reg(key: str, subkey: str, entry: Optional[str] = None):
        """
        Reads the given registry
        """
        # Registry reads should always be considered potentially dangerous reads
        _check_call(os.sep, IOType.Read)
        _read_reg(key, subkey, entry)
