# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3
"""
Module that interacts with the portmod config file

Files are stored both in the portmod local directory and in the profile directory tree,
with the user's config file overriding and extending defaults set by the profile
"""

from typing import Dict, Optional
import os
import string
import sys
from copy import deepcopy
from functools import lru_cache
from textwrap import fill
from .globals import env, get_version
from .repo.profiles import profile_parents, profile_exists
from .repo.flags import collapse_flags
from .l10n import l10n

__COLLAPSE_KEYS = {
    "USE",
    "ACCEPT_LICENSE",
    "ACCEPT_KEYWORDS",
    "INFO_VARS",
    "USE_EXPAND",
    "USE_EXPAND_HIDDEN",
    "PROFILE_ONLY_VARIABLES",
    "CACHE_FIELDS",
}
__OVERRIDE_KEYS = {
    "ARCH",
    "TEXTURE_SIZE",
    "PORTMOD_MIRRORS",
    "CASE_INSENSITIVE_FILES",
    "EXEC_PATH",
    "OMWMERGE_DEFAULT_OPTS",
}


def comment_wrap(text: str) -> str:
    return "\n".join(
        [
            fill(paragraph, width=80, initial_indent="# ", subsequent_indent="# ")
            # Squelch text together as one paragraph, except for double linebreaks, which define
            # new paragraphs
            for paragraph in text.split("\n\n")
        ]
    )


def create_config_placeholder():
    """
    Creates a placeholder config file to help the user initialize their
    config file for the first time
    """
    os.makedirs(env.PORTMOD_CONFIG_DIR, exist_ok=True)
    version = get_version()
    with open(env.PORTMOD_CONFIG, "w") as file:
        config_string = (
            # FIXME: Depending on how the wiki is localized, we may need to have wiki_page included in the localization
            # For now it is excluded so that it can be changed more easily across localizations
            comment_wrap(
                l10n(
                    "config-placeholder-header",
                    version=version,
                    info_command="`omwmerge --info`",
                    wiki_page="https://gitlab.com/portmod/portmod/wikis/Portmod-Config",
                )
            )
            + "\n\n"
            + comment_wrap(l10n("config-placeholder-global-use"))
            + '\n# USE=""\n\n'
            + comment_wrap(l10n("config-placeholder-texture-size", default="min"))
            + '\n# TEXTURE_SIZE="min"\n\n'
            + comment_wrap(l10n("config-placeholder-accept-keywords"))
            + '\n# ACCEPT_KEYWORDS="openmw"\n\n'
            + comment_wrap(l10n("config-placeholder-accept-license"))
            + '\n# ACCEPT_LICENSE="* -EULA"\n\n'
            + comment_wrap(l10n("config-placeholder-openmw-config"))
            + "\n\n"
            + comment_wrap(l10n("config-placeholder-morrowind-path"))
        )
        print(config_string, file=file)


def read_config(path: str, old_config: Dict, *, user: bool = False) -> Dict:
    """
    Reads a config file and converts the relevant fields into a dictionary
    """
    # Slow import
    from RestrictedPython import compile_restricted

    with open(path, "r") as file:
        config = file.read()

    if sys.platform == "win32":
        config = config.replace("\\", "\\\\")

    from .repo.loader import SAFE_GLOBALS, Policy

    byte_code = compile_restricted(config, filename=path, mode="exec", policy=Policy)

    glob = deepcopy(SAFE_GLOBALS)
    glob["__builtins__"]["join"] = os.path.join
    new_config = old_config.copy()
    try:
        exec(byte_code, glob, new_config)
    except NameError as e:
        print(l10n("exec-error", error=e, file=path))
    except SyntaxError as e:
        print(l10n("exec-error", error=e, file=path))

    merged = old_config.copy()

    def line_of_key(key: str) -> Optional[int]:
        for index, line in enumerate(config.split("\n")):
            if key in line:
                return index
        return None

    def profile_only(key):
        nonlocal new_config, old_config, merged
        if (
            user
            and key in merged.get("PROFILE_ONLY_VARIABLES", [])
            and new_config.get(key) is not None
            and new_config.get(key) != old_config.get(key)
        ):
            raise UserWarning(
                f"{path}:{line_of_key(key)}\n" + l10n("reserved-variable", key=key)
            )

    for key in __COLLAPSE_KEYS:
        profile_only(key)

        if isinstance(new_config.get(key, ""), str):
            new_config[key] = set(new_config.get(key, "").split())
        merged[key] = collapse_flags(merged.get(key, set()), new_config.get(key, set()))

    for key in __OVERRIDE_KEYS:
        profile_only(key)

        if key in new_config and new_config[key]:
            merged[key] = new_config.get(key)

    for key in old_config.keys() | new_config.keys():
        if (
            user
            and key in merged.get("PROFILE_ONLY_VARIABLES", [])
            and new_config.get(key) is not None
            and new_config.get(key) != old_config.get(key)
        ):
            raise UserWarning(
                f"{path}:{line_of_key(key)}\n" + l10n("reserved-variable", key=key)
            )

        if key not in __COLLAPSE_KEYS | __OVERRIDE_KEYS:
            if key in new_config:
                merged[key] = new_config[key]
                # Add user-defined variables as environment variables
                # We don't want profiles to be able to change environment variables
                # to prevent them from making malicious changes
                if user and key not in os.environ and isinstance(new_config[key], str):
                    os.environ[key] = new_config[key]
            else:
                merged[key] = old_config[key]

    return merged


@lru_cache(maxsize=None)
def get_config() -> Dict:
    """
    Parses the user's configuration, overriding defaults from their profile
    """
    total_config = {
        # Default cannot be set in profile due to the value depending on platform
        "PLATFORM": sys.platform,
    }

    if sys.platform == "win32":
        import ctypes.wintypes

        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value

        __BUF = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(
            None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, __BUF
        )
        total_config["PERSONAL"] = __BUF.value

    if profile_exists():
        for parent in profile_parents():
            path = os.path.join(parent, "defaults.conf")
            if os.path.exists(path):
                total_config = read_config(path, total_config)

    if os.path.exists(env.PORTMOD_CONFIG):
        total_config = read_config(env.PORTMOD_CONFIG, total_config, user=True)
    else:
        create_config_placeholder()

    # Apply environment variables onto config
    for key in __OVERRIDE_KEYS:
        if key in os.environ:
            if key not in total_config.get("PROFILE_ONLY_VARIABLES", []):
                total_config[key] = os.environ[key]
        elif key in total_config:
            os.environ[key] = str(total_config[key])

        if key not in total_config:
            total_config[key] = ""

    for key in __COLLAPSE_KEYS:
        if key in os.environ:
            if key not in total_config.get("PROFILE_ONLY_VARIABLES", []):
                total_config[key] = collapse_flags(
                    total_config.get(key, set()), os.environ[key].split()
                )
        elif key in total_config:
            os.environ[key] = " ".join(total_config[key])

        if key not in total_config:
            total_config[key] = set()

    to_remove = []
    for key in total_config:
        # All keys can use ${NAME} substitutions to use the final value
        #    instead of the current value of a field
        if isinstance(total_config[key], str):
            total_config[key] = string.Template(total_config[key]).substitute(
                total_config
            )
        elif isinstance(total_config[key], list):
            for index, elem in enumerate(total_config[key]):
                if isinstance(elem, str):
                    total_config[key][index] = string.Template(elem).substitute(
                        total_config
                    )
        elif isinstance(total_config[key], set):
            newset = set()
            for elem in total_config[key]:
                if isinstance(elem, str):
                    newset.add(string.Template(elem).substitute(total_config))
                else:
                    newset.add(elem)
            total_config[key] = newset

    for key in to_remove:
        del total_config[key]

    return total_config


def config_to_string(config: Dict) -> str:
    """
    Prints the given dictionary config as a string

    The resulting string is suitable for reading by read_config
    """
    lines = []
    for key in sorted(config):
        if isinstance(config[key], set) or isinstance(config[key], list):
            lines.append("{} = {}".format(key, " ".join(sorted(config[key]))))
        else:
            lines.append("{} = {}".format(key, config[key]))
    return "\n".join(lines)
