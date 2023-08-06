# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for performing bulk queries on the mod database and repositories
"""

from typing import AbstractSet, Dict, Generator, Iterable, List, Optional, Tuple, Union
import argparse
import re
import sys
import traceback
import os
from logging import info, error
from .globals import env
from .colour import green, lgreen, blue, bright, lblue, red, yellow
from .config import get_config
from .pybuild import Pybuild
from .repo.manifest import get_total_download_size
from .repo.loader import load_all, load_all_installed, load_installed_mod, load_mod
from .repo.util import get_newest_mod
from .repo.atom import Atom, atom_sat
from .repo.use import use_reduce, get_use, get_use_expand
from .repo.metadata import (
    get_mod_metadata,
    get_global_use,
    get_use_expand_values,
)
from .repo.keywords import get_unstable_flag
from .repo.usestr import parse_usestr
from .repos import get_repo
from .l10n import l10n


def get_maintainer_string(maintainers: Union[List[str], str]) -> str:
    def list_maintainers_to_human_strings(maintainers):
        """ return the list of maintainers as a human readible string """
        result = ""
        for maintainer_id in range(len(maintainers)):
            maintainer = str(maintainers[maintainer_id])
            if maintainer_id >= len(maintainers) - 1:  # the last
                result += maintainer
            elif maintainer_id >= len(maintainers) - 2:  # the second last
                result += maintainer + " and "
            else:
                result += maintainer + ", "
        return result

    if not isinstance(maintainers, list):
        maintainers = [maintainers]

    return list_maintainers_to_human_strings(maintainers)


def print_depgraph(
    mod: Pybuild, level: int, level_limit: int, seen: AbstractSet[Pybuild] = frozenset()
) -> int:
    """
    Recursively prints the dependency graph for the given mod.

    Note that use conditionals and or statements are ignored.
    This prints out all possible dependencies, not actual dependencies.
    """
    if level > level_limit:
        return level - 1

    deps = parse_usestr(mod.DEPEND + " " + mod.RDEPEND, token_class=Atom)
    max_level = level

    seen = set(seen)

    def print_token(token, conditional=None):
        atom = Atom(token)
        mod = get_newest_mod(load_mod(atom))
        enabled, _ = get_use(mod)

        def colour(flag):
            if flag.rstrip("?").lstrip("-!") in enabled:
                return bright(red(flag))
            return bright(blue(flag))

        use = map(colour, atom.USE)
        use_str = ""
        if atom.USE:
            use_str = f'[{" ".join(use)}]'

        if conditional:
            dep = f"( {conditional} ( {atom.strip_use()} ) ) "
        else:
            dep = f"({atom.strip_use()}) "

        print(" " * (level + 1) + f"-- {bright(green(mod.ATOM.CMF))} " + dep + use_str)
        if mod in seen:
            print(" " * level + "-- " + l10n("omit-already-displayed-tree"))
            return level
        else:
            seen.add(mod)
            return print_depgraph(mod, level + 1, level_limit, seen)

    for token in deps:
        if isinstance(token, list):
            if token[0] == "||":
                for inner_token in token[1:]:
                    max_level = max(level, print_token(inner_token))
            elif token[0].endswith("?"):
                for inner_token in token[1:]:
                    max_level = max(level, print_token(inner_token, token[0]))
            else:
                for inner_token in token:
                    max_level = max(level, print_token(inner_token))
        else:
            max_level = max(level, print_token(token))

    return max_level


def compose(*functions):
    """
    Composes the given single-argument functions
    """

    def inner(arg):
        for func in reversed(functions):
            arg = func(arg)
        return arg

    return inner


def str_strip(value: str) -> str:
    return re.sub("(( +- +)|(:))", "", value)


def str_squelch_sep(value: str) -> str:
    return re.sub(r"[-_\s]+", " ", value)


def query(
    fields: Union[str, Iterable],
    value: str,
    strip: bool = False,
    squelch_sep: bool = False,
    insensitive: bool = False,
    installed: bool = False,
) -> Generator[Pybuild, None, None]:
    """
    Finds mods that contain the given value in the given field
    """

    def func(val: str) -> str:
        result = val
        if insensitive:
            result = result.lower()
        if strip:
            result = str_strip(result)
        if squelch_sep:
            result = str_squelch_sep(result)
        return result

    search = func(value)

    if installed:
        mods = [mod for group in load_all_installed().values() for mod in group]
    else:
        mods = load_all()

    for mod in mods:
        if isinstance(fields, str):
            if hasattr(mod, fields) and search in func(getattr(mod, fields)):
                yield mod
        else:
            if any(
                hasattr(mod, field) and search in func(getattr(mod, field))
                for field in fields
            ):
                yield mod


def query_depends(atom: Atom, all_mods=False) -> List[Tuple[Atom, str]]:
    """
    Finds mods that depend on the given atom
    """
    if all_mods:
        mods = load_all()
    else:
        mods = [mod for group in load_all_installed().values() for mod in group]

    depends = []
    for mod in mods:
        if not all_mods:
            enabled, disabled = get_use(mod)
            atoms = use_reduce(
                mod.RDEPEND, enabled, disabled, token_class=Atom, flat=True
            )
        else:
            atoms = use_reduce(mod.RDEPEND, token_class=Atom, matchall=True, flat=True)

        for dep_atom in atoms:
            if dep_atom != "||" and atom_sat(dep_atom, atom):
                depends.append((mod.ATOM, dep_atom))
    return depends


def get_flag_string(
    name: Optional[str],
    enabled: Iterable[str],
    disabled: Iterable[str],
    installed: Optional[AbstractSet[str]] = None,
    *,
    verbose: bool = True,
    display_minuses=True,
):
    """
    Displays flag configuration

    Enabled flags are displayed as blue
    If the installed flag list is passed, flags that differ from the
    installed set will be green
    if name is None, the name prefix will be omitted and no quotes will
    surround the flags
    """

    def disable(string: str) -> str:
        if display_minuses:
            return "-" + string
        return string

    flags = []
    for flag in sorted(enabled):
        if installed is not None and flag not in installed:
            flags.append(bright(lgreen(flag)))
        elif verbose:
            flags.append(red(bright(flag)))

    for flag in sorted(disabled):
        if installed is not None and flag in installed:
            flags.append(bright(lgreen(disable(flag))))
        elif verbose:
            if display_minuses:
                flags.append(blue(disable(flag)))
            else:
                flags.append(lblue(disable(flag)))

    inner = " ".join(flags)

    if not flags:
        return None

    if name:
        return f'{name}="{inner}"'

    return inner


def display_search_results(
    mods: Iterable[Pybuild], summarize: bool = True, file=sys.stdout
):
    """
    Prettily formats a list of mods for use in search results
    """
    groupedmods: Dict[str, List[Pybuild]] = {}
    for mod in mods:
        if groupedmods.get(mod.CMN) is None:
            groupedmods[mod.CMN] = [mod]
        else:
            groupedmods[mod.CMN].append(mod)

    sortedgroups = sorted(groupedmods.values(), key=lambda group: group[0].NAME)

    for group in sortedgroups:
        sortedmods = sorted(group, key=lambda mod: mod.MV)
        newest = get_newest_mod(group)
        installed = load_installed_mod(Atom(newest.CMN))
        download = get_total_download_size([newest])

        if installed is not None:
            installed_str = blue(bright(installed.MV))

            flags = {flag.lstrip("+") for flag in installed.IUSE if "_" not in flag}
            usestr = get_flag_string(
                None, installed.INSTALLED_USE & flags, flags - installed.INSTALLED_USE
            )
            texture_options = {
                size
                for mod in group
                for size in use_reduce(
                    installed.TEXTURE_SIZES, matchall=True, flat=True
                )
            }
            texture = next(
                (
                    use.lstrip("texture_size_")
                    for use in installed.INSTALLED_USE
                    if use.startswith("texture_size_")
                ),
                None,
            )
            if isinstance(texture, str):
                texture_string = get_flag_string(
                    "TEXTURE_SIZE", [texture], texture_options - {texture}
                )
            else:
                texture_string = None
            use_expand_strings = []
            for use in get_config().get("USE_EXPAND", []):
                if use in get_config().get("USE_EXPAND_HIDDEN", []):
                    continue
                enabled_expand, disabled_expand = get_use_expand(installed, use)
                if enabled_expand or disabled_expand:
                    string = get_flag_string(use, enabled_expand, disabled_expand, None)
                    use_expand_strings.append(string)

            installed_str += (
                " {"
                + " ".join(
                    list(filter(None, [usestr, texture_string] + use_expand_strings))
                )
                + "}"
            )
        else:
            installed_str = "not installed"

        # List of version numbers, prefixed by either (~) or ** depending on
        # keyword for user's arch. Followed by use flags, including use expand
        version_str = ""
        versions = []
        ARCH = get_config()["ARCH"]
        for mod in sortedmods:
            if ARCH in mod.KEYWORDS:
                versions.append(green(mod.MV))
            elif "~" + ARCH in mod.KEYWORDS:
                versions.append(yellow("(~)" + mod.MV))
            else:
                versions.append(red("**" + mod.MV))
        version_str = " ".join(versions)
        flags = {
            flag.lstrip("+") for mod in group for flag in mod.IUSE if "_" not in flag
        }
        usestr = get_flag_string(None, [], flags, display_minuses=False)
        texture_options = {
            size
            for mod in group
            for size in use_reduce(mod.TEXTURE_SIZES, matchall=True, flat=True)
        }
        texture_string = get_flag_string(
            "TEXTURE_SIZE", [], texture_options, display_minuses=False
        )
        use_expand_strings = []
        for use in get_config().get("USE_EXPAND", []):
            if use in get_config().get("USE_EXPAND_HIDDEN", []):
                continue
            flags = {
                re.sub(f"^{use.lower()}_", "", flag)
                for flag in mod.IUSE_EFFECTIVE
                for mod in group
                if flag.startswith(f"{use.lower()}_")
            }
            if flags:
                string = get_flag_string(use, [], flags, None, display_minuses=False)
                use_expand_strings.append(string)

        version_str += (
            " {"
            + " ".join(
                list(filter(None, [usestr, texture_string] + use_expand_strings))
            )
            + "}"
        )

        # If there are multiple URLs, remove any formatting from the pybuild and
        # add padding
        homepage_str = "\n                 ".join(newest.HOMEPAGE.split())
        mod_metadata = get_mod_metadata(mod)

        print(
            "{}  {}".format(green("*"), bright(newest.CMN)),
            "       {} {}".format(green(l10n("package-name")), mod.NAME),
            "       {} {}".format(
                green(l10n("package-available-versions")), version_str
            ),
            "       {} {}".format(
                green(l10n("package-installed-version")), installed_str
            ),
            "       {} {}".format(green(l10n("package-size-of-files")), download),
            "       {} {}".format(green(l10n("package-homepage")), homepage_str),
            "       {} {}".format(
                green(l10n("package-description")), str_squelch_sep(newest.DESC)
            ),
            "       {} {}".format(green(l10n("package-license")), newest.LICENSE),
            sep="\n",
            file=file,
        )

        if mod_metadata and mod_metadata.upstream:
            maintainers = mod_metadata.upstream.maintainer
            if maintainers:
                maintainers_display_strings = get_maintainer_string(maintainers)
                print(
                    "       {} {}".format(
                        green(l10n("package-upstream-author")),
                        maintainers_display_strings,
                    ),
                    file=file,
                )

        print(file=file)

    if summarize:
        print("\n" + l10n("packages-found", num=len(sortedgroups)), file=file)


def subcommand(*sub_args, parent):
    def decorator(func):
        parser = parent.add_parser(
            func.__name__,
            description=l10n("query-{func.__name__}-help"),
            help=l10n("query-{func.__name__}-help").strip().splitlines()[0],
        )
        for args, kwargs in sub_args:
            parser.add_argument(*args, **kwargs)
        parser.set_defaults(func=func)

    return decorator


def argument(*name_or_flags, **kwargs):
    return name_or_flags, kwargs


def query_main():
    """
    Main function for omwquery executable
    """
    parser = argparse.ArgumentParser(description=l10n("query-help"))
    parser.add_argument("--debug", help=l10n("debug-help"), action="store_true")
    subparsers = parser.add_subparsers(title=l10n("query-subcommands-title"))
    parser.add_argument("-a", "--all", help=l10n("query-all-help"), action="store_true")

    @subcommand(
        argument("ATOM", help=l10n("query-depends-atom-help")), parent=subparsers
    )
    def depends(args):
        """List all packages directly depending on ATOM"""
        print(" * These mods depend on {}:".format(bright(args.ATOM)))
        for mod_atom, dep_atom in query_depends(Atom(args.ATOM), args.all):
            print("{} ({})".format(green(mod_atom), dep_atom))

    @subcommand(
        argument("var", help=l10n("query-has-var-help")),
        argument("expr", default="", nargs="?", help=l10n("query-has-expr-help")),
        parent=subparsers,
    )
    def has(args):
        """
        List all packages matching variable.

        This can only be used to scan variables in the base Pybuild spec, not custom
        fields declared by specific Pybuilds or their superclasses.
        """
        if args.expr:
            info(
                " * "
                + l10n("query-has-searching-msg", var=args.var)
                + f" '{bright(args.expr)}'"
            )
        else:
            info(" * " + l10n("query-has-searching-msg", var=args.var))
        for mod in query(args.var, args.expr, installed=not args.all, insensitive=True):
            flags = [" ", " "]
            if mod.INSTALLED or load_installed_mod(Atom(mod.ATOM.CMF)):
                flags[0] = "I"
            flags[1] = get_unstable_flag(mod) or " "
            print(f'[{"".join(flags)}] {green(mod.ATOM.CMF)}')

    @subcommand(argument("use", help=l10n("query-hasuse-help")), parent=subparsers)
    def hasuse(args):
        """
        List all packages that declare the given use flag.

        Note that this only includes those with the flag in their IUSE
        field and inherited flags through IUSE_EFFECTIVE will not be counted
        """
        info(" * " + l10n("query-hasuse-searching-msg", use=args.use))
        for mod in query("IUSE", args.use, installed=not args.all):
            flags = [" ", " "]
            if mod.INSTALLED or load_installed_mod(Atom(mod.ATOM.CMF)):
                flags[0] = "I"
            flags[1] = get_unstable_flag(mod) or " "
            print(f'[{"".join(flags)}] {green(mod.ATOM.CMF)}')

    @subcommand(argument("atom", help=l10n("query-uses-atom-help")), parent=subparsers)
    def uses(args):
        """Display use flags and their descriptions"""
        modlist = load_mod(Atom(args.atom))
        if not modlist:
            error(l10n("not-found", atom=args.atom))
            return

        legend_space = " " * len(l10n("query-uses-legend"))
        padding = max(len(l10n("query-uses-final")), len(l10n("query-uses-installed")))
        print(
            f'[ {l10n("query-uses-legend")}: {bright("U")} - {l10n("query-uses-final").ljust(padding)}]'
        )
        print(
            f'[ {legend_space}: {bright("I")} - {l10n("query-uses-installed").ljust(padding)}]'
        )
        print(" * " + l10n("query-uses-found", atom=args.atom))
        flags = {}
        for mod in modlist:
            repo_root = get_repo(mod.REPO).location

            global_use = get_global_use(repo_root)
            metadata = get_mod_metadata(mod)

            enabled, _ = get_use(mod)
            for flag in mod.IUSE_EFFECTIVE:
                installed = False
                if mod.INSTALLED:
                    installed = flag in mod.INSTALLED_USE

                if metadata and flag in metadata.use:
                    desc = metadata.use[flag]
                elif flag in global_use:
                    desc = global_use[flag]
                elif "_" in flag and not flag.startswith("texture_size_"):  # USE_EXPAND
                    use_expand = flag.rsplit("_", 1)[0]
                    desc = (
                        get_use_expand_values(repo_root, use_expand).get(
                            flag.replace(use_expand + "_", "")
                        )
                        + " "
                        + l10n("use-expand")
                    )
                elif flag.startswith("texture_size_"):
                    desc = l10n(
                        "texture-size-desc", size=flag.replace("texture_size_", "")
                    )

                flags[flag] = (
                    flag in enabled,
                    installed,
                    desc,
                )

        print(" U I")

        maxlen = max([len(bright(blue(flag))) for flag in flags]) + 2
        for flag in sorted(flags):
            enabled, installed, desc = flags[flag]
            enabled_flags = ["-", "-"]
            if enabled:
                enabled_flags[0] = "+"
            if installed:
                enabled_flags[1] = "+"

            colour = blue
            if enabled:
                colour = red

            print(
                f' {" ".join(enabled_flags)} '
                + f"{bright(colour(flag))}".ljust(maxlen)
                + f": {desc}"
            )

    @subcommand(argument("atom", help=l10n("query-meta-atom-help")), parent=subparsers)
    def meta(args):
        """Display metadata for a package"""
        modlist = load_mod(Atom(args.atom))
        if not modlist:
            raise Exception(l10n("not-found", atom=args.atom))

        mods = {}
        for mod in modlist:
            if mod.CMN in mods:
                mods[mod.CMN].append(mod)
            else:
                mods[mod.CMN] = [mod]

        for modname in mods:
            metadata = {}
            for mod in mods[modname]:
                mod_metadata = get_mod_metadata(mod)
                if mod_metadata:
                    metadata = mod_metadata

            print(f" * {bright(green(modname))}")
            if not metadata:
                continue

            if metadata.maintainer:
                maintainer_string = get_maintainer_string(metadata.maintainer)
                print(l10n("package-maintainer") + "\t", maintainer_string)

            if metadata.upstream:
                upstream = metadata.upstream
                first = True
                for key in ["maintainer", "changelog", "doc", "bugs_to"]:
                    if hasattr(upstream, key) and getattr(upstream, key):
                        string = getattr(upstream, key)
                        if key == "maintainer":
                            string = get_maintainer_string(string)

                        if first:
                            print(
                                l10n("package-upstream")
                                + "\t "
                                + key.title()
                                + ":\t"
                                + string
                            )
                            first = False
                        elif key == "doc":
                            print("\t\t " + key.title() + ":\t\t" + string)
                        else:
                            print("\t\t " + key.title() + ":\t" + string)

            print(l10n("package-homepage") + "\t", " ".join(mod.HOMEPAGE.split()))
            for mod in mods[modname]:
                path = os.path.join(env.MOD_DIR, mod.CATEGORY, mod.MN)
                if mod.INSTALLED and os.path.exists(path):
                    print(l10n("package-location") + "\t", path)
            for mod in mods[modname]:
                print(
                    l10n("package-keywords") + "\t",
                    mod.MV + ":",
                    " ".join(mod.KEYWORDS),
                )
            print(l10n("package-license") + "\t", " ".join(mod.LICENSE.split()))

    @subcommand(
        argument("atom", help=l10n("package-depgraph-atom-help")),
        argument("--depth", type=int, help=l10n("query-depgraph-depth-help")),
        parent=subparsers,
    )
    def depgraph(args):
        """Display dependency graph for package""" ""
        modlist = load_mod(Atom(args.atom))
        if not modlist:
            raise Exception(l10n("not-found", atom=args.atom))

        for mod in modlist:
            print(" * " + l10n("query-depgraph-depgraph", atom=mod.ATOM))
            max_depth = print_depgraph(mod, 1, args.depth or 10)
            print(" " + l10n("query-depgraph-max-depth") + f"({max_depth})")
            print()

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    if args.debug:
        env.DEBUG = True
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            traceback.print_exc()
            error("{}".format(e))
            sys.exit(1)
