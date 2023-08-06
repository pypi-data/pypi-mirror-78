# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import re
from portmod.portmod import get_masters as native_get_masters


def get_masters(file):
    """
    Detects masters for the given file
    """
    _, ext = os.path.splitext(file)
    if re.match(r"\.(esp|esm|omwaddon|omwgame)", ext, re.IGNORECASE):
        return set(native_get_masters(file))
    return set()
