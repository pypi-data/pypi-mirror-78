# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

from typing import Iterable, Optional, Set, Tuple

import sys
import os
import argparse
import io
import traceback
import shutil
import logging
import configparser
import getpass
from logging import error, info, warning
from packaging import version

from colorama import Fore
from portmod.repos import Repo
from portmod.globals import env, get_version
from portmod.repo.atom import Atom, atom_sat, InvalidAtom
from portmod.repo.loader import (
    load_mod,
    full_load_file,
    load_installed_mod,
    load_all_installed,
)
from portmod.transactions import (
    generate_transactions,
    print_transactions,
    sort_transactions,
    Trans,
    Transactions,
    UseDep,
)
from portmod.repo.deps import resolve, PackageDoesNotExist, AmbigiousAtom, DepError
from portmod.repo.util import select_mod, KeywordDep, LicenseDep
from portmod.repo.sets import add_set, get_set, remove_set
from portmod.repo.keywords import add_keyword
from portmod.colour import lblue, colour, green, lgreen, red, bright
from portmod.mod import install_mod, remove_mod
from portmod.prompt import prompt_bool
from portmod.repo.metadata import get_repo_root
from portmod.query import query, display_search_results
from portmod.repo.download import is_downloaded, fetchable, find_download
from portmod.repo.manifest import create_manifest
from portmod.news import update_news, display_unread_message
from .vfs import (
    sort_vfs,
    require_vfs_sort,
    clear_vfs_sort,
    vfs_needs_sorting,
)
from .tsort import CycleException
from .repo.use import add_use
from .repo.usestr import check_required_use
from .repo.profiles import get_system
from .config import config_to_string, get_config
from .pybuild import FullPybuild
from .repos import has_repo
from .log import init_logger, add_logging_arguments
from .modules import require_module_updates, update_modules, clear_module_updates
from .l10n import l10n
from .util import onerror


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_args():
    parser = argparse.ArgumentParser(description=l10n("description"))
    parser.add_argument("mods", metavar="PKG", help=l10n("package-help"), nargs="*")
    parser.add_argument("--sync", help=l10n("sync-help"), action="store_true")
    parser.add_argument(
        "-c", "--depclean", help=l10n("depclean-help"), action="store_true"
    )
    parser.add_argument(
        "-x", "--auto-depclean", help=l10n("auto-depclean-help"), action="store_true"
    )
    parser.add_argument(
        "-C", "--unmerge", help=l10n("unmerge-help"), action="store_true"
    )
    parser.add_argument(
        "--no-confirm", help=l10n("no-confirm-help"), action="store_true"
    )
    parser.add_argument(
        "-1", "--oneshot", help=l10n("oneshot-help"), action="store_true"
    )
    parser.add_argument("-O", "--nodeps", help=l10n("nodeps-help"), action="store_true")
    add_logging_arguments(parser)
    parser.add_argument(
        "-n", "--noreplace", help=l10n("noreplace-help"), action="store_true"
    )
    parser.add_argument("-u", "--update", help=l10n("update-help"), action="store_true")
    parser.add_argument("-N", "--newuse", help=l10n("newuse-help"), action="store_true")
    parser.add_argument(
        "-e", "--emptytree", help=l10n("emptytree-help"), action="store_true"
    )
    parser.add_argument("-D", "--deep", help=l10n("deep-help"), action="store_true")
    parser.add_argument("-s", "--search", help=l10n("search-help"), action="store_true")
    parser.add_argument(
        "-S", "--searchdesc", help=l10n("searchdesc-help"), action="store_true"
    )
    parser.add_argument(
        "-w",
        "--select",
        type=str2bool,
        nargs="?",
        const=True,
        default=None,
        help=l10n("merge-select-help"),
    )
    parser.add_argument(
        "--deselect",
        type=str2bool,
        nargs="?",
        const=True,
        default=None,
        help=l10n("merge-deselect-help"),
    )
    # TODO: Ensure that installed mods database matches mods that are actually installed
    parser.add_argument("--validate", help=l10n("validate-help"), action="store_true")
    parser.add_argument("--sort-vfs", help=l10n("sort-vfs-help"), action="store_true")
    parser.add_argument("--debug", help=l10n("merge-debug-help"), action="store_true")
    parser.add_argument(
        "--ignore-default-opts",
        help=l10n("ignore-default-opts-help"),
        action="store_true",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--version", help=l10n("version-help"), action="store_true")
    group.add_argument("--info", help=l10n("info-help"), action="store_true")
    try:
        import argcomplete  # pylint: disable=import-error

        argcomplete.autocomplete(parser)
    except ModuleNotFoundError:
        pass

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # Ensure that we read config entries into os.environ
    get_config()

    if "--ignore-default-opts" in sys.argv:
        args = sys.argv[1:]
    else:
        args = sys.argv[1:] + os.environ.get("OMWMERGE_DEFAULT_OPTS", "").split()
    return parser.parse_args(args)


def sync():
    # Slow imports
    import git

    # Ensure that INSTALLED_DB exists
    if not os.path.exists(env.INSTALLED_DB):
        # Initialize as git repo
        os.makedirs(env.INSTALLED_DB)
        gitrepo = git.Repo.init(env.INSTALLED_DB)
        # This repository is for local purposes only.
        # We don't want to worry about prompts for the user's gpg key password
        localconfig = gitrepo.config_writer()
        localconfig.set_value("commit", "gpgsign", False)
        USER = getpass.getuser()

        try:
            # May throw TypeError if GitPython<3.0.5
            globalconfig = git.config.GitConfigParser()
            globalconfig.get_value("user", "name")
            globalconfig.get_value("user", "email")
        except (TypeError, configparser.NoOptionError, configparser.NoSectionError):
            # Set the user name and email if they aren't in a global config
            localconfig.set_value("user", "name", f"{USER}")
            localconfig.set_value("user", "email", f"{USER}@example.com")

        localconfig.release()

    for repo in env.REPOS:
        if repo.auto_sync and repo.sync_type == "git":

            if os.path.exists(repo.location):
                info(l10n("syncing-repo", repo=repo.name))
                gitrepo = git.Repo.init(repo.location)
                current = gitrepo.head.commit

                # Remote location has changed. Update gitrepo to match
                if gitrepo.remotes.origin.url != repo.sync_uri:
                    gitrepo.remotes.origin.set_url(repo.sync_uri)

                gitrepo.remotes.origin.fetch()
                gitrepo.head.reset("origin/master", True, True)

                for diff in current.diff("HEAD"):
                    if diff.renamed_file:
                        print(
                            "{} {} -> {}".format(
                                diff.change_type, diff.a_path, diff.b_path
                            )
                        )
                    if diff.deleted_file:
                        print("{} {}".format(diff.change_type, diff.a_path))
                        if diff.a_path.endswith(".pybuild"):
                            # Remove from pybuild cache
                            parts = diff.a_path.split("/")
                            category = parts[0]
                            file = parts[-1].lstrip(".pybuild")
                            path = os.path.join(
                                env.PYBUILD_CACHE_DIR, repo.name, category, file
                            )
                            if os.path.exists(path):
                                os.remove(path)
                    else:
                        print("{} {}".format(diff.change_type, diff.b_path))

                tags = []
                for tag in gitrepo.tags:
                    # Valid tags must have the tag commit be the merge base
                    # A merge base further back indicates a branch point
                    if tag.name.startswith("portmod_v"):
                        base = gitrepo.merge_base(gitrepo.head.commit, tag.commit)
                        if base and base[0] == tag.commit:
                            tags.append(tag)

                this_version = version.parse(get_version())
                newest = max(
                    [version.parse(tag.name.lstrip("portmod_v")) for tag in tags]
                    + [this_version]
                )
                if newest != this_version and not env.TESTING:
                    warning(l10n("update-message"))
                    warning(l10n("current-version", version=this_version))
                    warning(l10n("new-version", version=newest))
                info(l10n("done-syncing-repo", repo=repo.name))
            else:
                git.Repo.clone_from(repo.sync_uri, repo.location)
                print(l10n("initialized-repository"))
        elif repo.auto_sync:
            error(
                l10n(
                    "invalid-sync-type",
                    type=repo.sync_type,
                    repo=repo.name,
                    supported="git",
                )
            )

    if os.path.exists(env.PYBUILD_CACHE_DIR):
        for repo in os.listdir(env.PYBUILD_CACHE_DIR):
            path = os.path.join(env.PYBUILD_CACHE_DIR, repo)
            if repo != "installed" and not has_repo(repo):
                print(l10n("cache-cleanup", repo=repo))
                shutil.rmtree(path)

    update_news()


def configure_mods(
    atoms: Iterable[str],
    *,
    delete: bool = False,
    depclean: bool = False,
    auto_depclean: bool = False,
    no_confirm: bool = False,
    oneshot: bool = False,
    verbose: bool = False,
    update: bool = False,
    newuse: bool = False,
    noreplace: bool = False,
    nodeps: bool = False,
    deselect: Optional[bool] = None,
    select: Optional[bool] = None,
    deep: bool = False,
    emptytree: bool = False,
):
    # Slow import
    import git

    # Ensure that we always get the config before performing operations on mods
    # This way the config settings will be available as environment variables.
    get_config()

    targetlist = list(atoms)
    for modstr in targetlist:
        if modstr.startswith("@"):
            # Atom is actually a set. Load set instead
            targetlist.extend(get_set(modstr.replace("@", "")))
            continue

    to_remove = set()
    if delete or depclean:
        for modstr in targetlist:
            if modstr.startswith("@"):
                continue

            skip = False
            atom = Atom(modstr)
            for system_atom in get_system():
                if atom_sat(system_atom, atom):
                    warning(l10n("skipping-system-package", atom=system_atom))
                    skip = True
                    break

            if not skip:
                to_remove.add(atom)

    atomlist = [
        Atom(modstr)
        for modstr in targetlist
        if modstr not in to_remove and not modstr.startswith("@")
    ]

    if delete:
        # Do nothing. We don't care about deps
        transactions = Transactions()
        for atom in to_remove:
            mod = load_installed_mod(atom)
            if not mod:
                raise Exception(l10n("not-installed", atom=atom))
            transactions.append(Trans.DELETE, mod)
    elif nodeps:
        fqatoms = []
        for atom in atomlist:
            mod, _ = select_mod(load_mod(atom))
            fqatoms.append(mod.ATOM)

        newselected: Set[Atom]
        if oneshot:
            newselected = set()
        else:
            newselected = {Atom(atom.CMN) for atom in fqatoms}

        transactions = generate_transactions(
            fqatoms, [], newselected, [], noreplace=noreplace, emptytree=emptytree
        )
    else:
        transactions = resolve(
            atomlist,
            to_remove,
            deep=deep
            or (depclean and not to_remove),  # No argument depclean implies deep
            update=update,
            newuse=newuse,
            noreplace=noreplace or depclean or update or newuse,
            depclean=auto_depclean or depclean,
            emptytree=emptytree,
        )

    transactions = sort_transactions(transactions)

    # Inform user of changes
    if transactions.mods:
        # Don't print transaction list when in quiet mode and no-confirm is passed
        if not no_confirm or logging.root.level < logging.WARN:
            if delete or depclean:
                print(l10n("to-remove"))
            else:
                print(l10n("to-install"))
            print_transactions(transactions, verbose=verbose)
            print()
    elif vfs_needs_sorting() and not transactions.mods:
        global_updates()
        info(l10n("nothing-else-to-do"))
        return
    elif not transactions.mods:
        info(l10n("nothing-to-do"))
        return

    if transactions.config:
        keyword_changes = list(
            filter(lambda x: isinstance(x, KeywordDep), transactions.config)
        )
        license_changes = list(
            filter(lambda x: isinstance(x, LicenseDep), transactions.config)
        )
        use_changes = list(filter(lambda x: isinstance(x, UseDep), transactions.config))
        if keyword_changes:
            print(l10n("necessary-keyword-changes"))
            for keyword in keyword_changes:
                if keyword.keyword.startswith("*"):
                    c = Fore.RED
                else:
                    c = Fore.YELLOW
                print(
                    "    {} {}".format(green(keyword.atom), colour(c, keyword.keyword))
                )

            if no_confirm or prompt_bool(l10n("apply-changes?")):
                for keyword in keyword_changes:
                    add_keyword(keyword.atom, keyword.keyword)
            else:
                return

        if license_changes:
            # TODO: For EULA licenses, display the license and prompt the user to accept
            print(l10n("necessary-license-changes"))
            for license in license_changes:
                print("    {} {}".format(green(license.atom), license.license))
            return

        if use_changes:
            print(l10n("necessary-flag-changes"))
            for use in use_changes:
                if use.flag.startswith("-") and use.oldvalue == use.flag.lstrip("-"):
                    print(
                        "    {} {} # {}".format(
                            lblue(use.atom), red(use.flag), l10n("enabled-comment")
                        )
                    )
                elif not use.flag.startswith("-") and use.oldvalue == "-" + use.flag:
                    print(
                        "    {} {} # {}".format(
                            green(use.atom), red(use.flag), l10n("disabled-comment")
                        )
                    )
                else:
                    print("    {} {}".format(green(use.atom), red(use.flag)))
            if no_confirm or prompt_bool(l10n("apply-changes-qn")):
                for use in use_changes:
                    add_use(use.flag.lstrip("-"), use.atom, use.flag.startswith("-"))
            else:
                return

    def print_restricted_fetch(transactions: Transactions):
        # Check for restricted fetch mods and print their nofetch notices
        for (trans, mod) in transactions.mods:
            if trans != Trans.DELETE:
                can_fetch = fetchable(mod)
                to_fetch = [
                    source
                    for source in mod.get_default_sources()
                    if find_download(source.name, source.hashes) is None
                ]
                if set(to_fetch) - set(can_fetch) and not is_downloaded(mod):
                    print(green(l10n("fetch-instructions", atom=mod.ATOM)))
                    mod.UNFETCHED = to_fetch
                    mod.A = mod.get_default_sources()
                    mod.USE = mod.get_use()[0]
                    mod.mod_nofetch()
                    del mod.UNFETCHED
                    print()

    print_restricted_fetch(transactions)

    tmp_dir = env.TMP_DIR
    # If TMP_DIR doesn't exist, either use the parent, or if that doesn't exist,
    # just create it
    if not os.path.exists(env.TMP_DIR):
        if os.path.exists(os.path.dirname(env.TMP_DIR)):
            tmp_dir = os.path.dirname(env.TMP_DIR)
        else:
            os.makedirs(tmp_dir, exist_ok=True)
    tmp_space = shutil.disk_usage(tmp_dir).free

    for (trans, mod) in transactions.mods:
        if trans != Trans.DELETE:
            # TODO: There are various variables that should be set on mod during mod_pretend
            mod.mod_pretend()

            for source in mod.get_default_sources():
                if source.size > 4 * tmp_space:
                    warning(
                        l10n(
                            "tmp-space-too-small",
                            dir=env.TMP_DIR,
                            free=tmp_space / 1024 / 1024,
                            size=source.size * 4 / 1024 / 1024,
                        )
                    )

    if not (no_confirm or prompt_bool(l10n("continue-qn"))):
        return

    err = None
    merged = Transactions()
    messages = []
    # Install (or remove) mods in order
    for trans, mod in transactions.mods:
        if trans == Trans.DELETE:
            remove_mod(mod)
            if deselect is None or deselect:
                if mod.CMN in get_set("world"):
                    info(">>> " + l10n("remove-from-world", atom=green(mod.CMN)))
                    remove_set("world", mod.CMN)
            merged.mods.append((trans, mod))
        elif install_mod(mod):
            if mod in transactions.new_selected and not oneshot:
                if mod.CMN not in get_set("world"):
                    info(">>> " + l10n("add-to-world", atom=green(mod.CMN)))
                    add_set("world", mod.CMN)
            merged.mods.append((trans, mod))
        else:
            # Unable to install mod. Aborting installing remaining mods
            err = mod.ATOM
            break

        mod_msg = []
        for msg in mod._warnings:
            mod_msg.append(("WARN", msg))
        for msg in mod._info:
            mod_msg.append(("INFO", msg))

        if mod_msg:
            messages.append((mod.ATOM.CMF, mod_msg))
        require_vfs_sort()
        require_module_updates()

    for pkg, msgs in messages:
        print()
        print(">>> " + l10n("pkg-messages", atom=bright(green(pkg))))
        for typ, msg in msgs:
            if typ == "WARN":
                warning(msg)
            elif typ == "INFO":
                info(msg)
        print()

    # Commit changes to installed database
    gitrepo = git.Repo.init(env.INSTALLED_DB)
    try:
        gitrepo.head.commit
    except ValueError:
        gitrepo.git.commit(m=l10n("initial-commit"))

    transstring = io.StringIO()
    print_transactions(merged, verbose=True, out=transstring, summarize=False)
    if gitrepo.git.diff("HEAD", cached=True):
        # There was an error. We report the mods that were successfully merged and
        # note that an error occurred, however we still commit anyway.
        if err:
            gitrepo.git.commit(
                m=(
                    l10n(
                        "merge-success-and-error", num=len(transactions.mods), atom=err
                    )
                    + "\n"
                    + transstring.getvalue()
                )
            )
        else:
            gitrepo.git.commit(
                m=(
                    l10n("merge-success", num=len(transactions.mods))
                    + "\n"
                    + transstring.getvalue()
                )
            )

    # Check if mods need to be added to rebuild set
    if plugin_changed(merged.mods):
        for mod in query("REBUILD", "ANY_PLUGIN", installed=True):
            if mod.ATOM not in [mod.ATOM for (trans, mod) in merged.mods]:
                add_set("rebuild", mod.CMN)

    # Check if mods were just modified and can be removed from the rebuild set
    # Any transaction type warrants removal, as they were either rebuilt,
    # and thus can be removed, or deleted, and no longer need to be rebuild
    for atom in get_set("rebuild"):
        installed_mod = load_installed_mod(atom)
        if not installed_mod or mod.CMN in [mod.CMN for (trans, mod) in merged.mods]:
            remove_set("rebuild", installed_mod.CMN)

    if get_set("rebuild"):
        warning(l10n("rebuild-message"))
        for atom in get_set("rebuild"):
            print("    {}".format(green(atom)))
        print(l10n("rebuild-prompt", command=lgreen("omwmerge @rebuild")))

    global_updates()


def plugin_changed(mods: Iterable[Tuple[Trans, FullPybuild]]):
    for (_, mod) in mods:
        for idir in mod.INSTALL_DIRS:
            for plug in getattr(idir, "PLUGINS", []):
                if check_required_use(
                    plug.REQUIRED_USE, mod.get_use()[0], mod.valid_use
                ) and check_required_use(
                    idir.REQUIRED_USE, mod.get_use()[0], mod.valid_use
                ):
                    return True


def global_updates():
    """Performs updates to global configuration"""
    # Update module set.
    for mod in get_set("modules", parent_dir=env.PORTMOD_LOCAL_DIR):
        if not load_installed_mod(Atom(mod)):
            # Note: safe because this doesn't modify the set returned by get_set
            remove_set("modules", mod, parent_dir=env.PORTMOD_LOCAL_DIR)

    for mod in load_all_installed(flat=True):
        if "module" in mod.PROPERTIES:
            add_set("modules", mod.CMN, parent_dir=env.PORTMOD_LOCAL_DIR)

    # Fix vfs ordering and update modules
    try:
        sort_vfs()
        clear_vfs_sort()
        update_modules()
        clear_module_updates()
    except CycleException as e:
        error(f"{e}")


def deselect(mods: Iterable[str], *, no_confirm: bool = False):
    all_to_remove = []

    for name in mods:
        atom = Atom(name)
        to_remove = []
        for mod in get_set("selected"):
            if atom_sat(mod, atom):
                to_remove.append(mod)

        if len(to_remove) == 1:
            info(">>> " + l10n("remove-from-world", atom=green(to_remove[0])))
            all_to_remove.append(to_remove[0])
        elif len(to_remove) > 1:
            raise AmbigiousAtom(atom, to_remove)

    if not all_to_remove:
        print(">>> " + l10n("no-matching-world-atom"))
        return

    if no_confirm or prompt_bool(bright(l10n("remove-from-world-qn"))):
        for mod in all_to_remove:
            remove_set("world", mod)


def filter_mods(mods):
    from portmod.pybuild import SHA512
    from portmod.repo.loader import load_all
    from portmod.repo.util import get_hash
    from shutil import move

    atoms = []
    os.makedirs(env.DOWNLOAD_DIR, exist_ok=True)

    for mod in mods:
        if os.path.isfile(mod):
            for atom in load_all():
                for source in atom.get_sources(matchall=True):
                    if get_hash(mod)[0] == source.hashes[SHA512]:
                        move(
                            mod,
                            os.path.join(env.DOWNLOAD_DIR, source.name),
                        )
                        atoms.append(atom.ATOM)
        else:
            atoms.append(mod)

    return atoms


def main():
    os.environ["PYTHONUNBUFFERED"] = "1"

    args = parse_args()
    atoms = filter_mods(args.mods)

    env.DEBUG = args.debug

    init_logger(args)

    if args.version:
        print(f"Portmod {get_version()}")

    if args.info:
        # Print config values
        config = get_config()
        if args.verbose:
            print(config_to_string(config))
        else:
            print(
                config_to_string(
                    {
                        entry: config[entry]
                        for entry in config
                        if entry in config["INFO_VARS"]
                    }
                )
            )
        # Print hardcoded portmod paths
        print(f"TMP_DIR = {env.TMP_DIR}")
        print(f"CACHE_DIR = {env.CACHE_DIR}")
        print(f"PORTMOD_CONFIG_DIR = {env.PORTMOD_CONFIG_DIR}")
        print(f"PORTMOD_LOCAL_DIR = {env.PORTMOD_LOCAL_DIR}")

    if args.validate:
        # Check that mods in the DB correspond to mods in the mods directory
        for category in os.listdir(env.INSTALLED_DB):
            if not category.startswith("."):
                for mod in os.listdir(os.path.join(env.INSTALLED_DB, category)):
                    # Check that mod is installed
                    if not os.path.exists(os.path.join(env.MOD_DIR, category, mod)):
                        error(
                            l10n("in-database-not-installed", atom=f"{category}/{mod}")
                        )

                    # Check that pybuild can be loaded
                    if not load_installed_mod(Atom(f"{category}/{mod}")):
                        error(l10n("installed-could-not-load"))

        # Check that all mods in the mod directory are also in the DB
        for category in os.listdir(env.MOD_DIR):
            for mod in os.listdir(os.path.join(env.MOD_DIR, category)):
                if not os.path.exists(os.path.join(env.INSTALLED_DB, category, mod)):
                    error(l10n("installed-not-in-database", atom=f"{category}/{mod}"))

    if args.sync:
        sync()

    if args.search:
        mods = query(
            ["NAME", "ATOM"],
            " ".join(atoms),
            strip=True,
            squelch_sep=True,
            insensitive=True,
        )
        display_search_results(mods)
        return

    if args.searchdesc:
        mods = query(
            ["NAME", "ATOM", "DESC"],
            " ".join(atoms),
            strip=True,
            squelch_sep=True,
            insensitive=True,
        )

        display_search_results(mods)
        return

    if args.nodeps and args.depclean:
        error(l10n("nodeps-depclean"))
        sys.exit(1)

    if atoms or args.depclean:
        # If deselect is supplied (is not None), only deselect if not removing.
        # If removing, remove normally, but deselect depending on supplied value.
        if args.deselect and not (args.unmerge or args.depclean):
            deselect(atoms, no_confirm=args.no_confirm)
        else:
            try:
                configure_mods(
                    atoms,
                    delete=args.unmerge,
                    depclean=args.depclean,
                    no_confirm=args.no_confirm,
                    oneshot=args.oneshot,
                    verbose=args.verbose,
                    update=args.update,
                    newuse=args.newuse,
                    noreplace=args.noreplace or args.update or args.newuse,
                    nodeps=args.nodeps,
                    deselect=args.deselect,
                    select=args.select,
                    auto_depclean=args.auto_depclean,
                    deep=args.deep,
                    emptytree=args.emptytree,
                )

                # Note: When execeptions occur, TMP_DIR should be preserved
                if not env.DEBUG and os.path.exists(env.TMP_DIR):
                    shutil.rmtree(env.TMP_DIR, onerror=onerror)
                    info(">>> " + l10n("cleaned-up", dir=env.TMP_DIR))
            except (InvalidAtom, PackageDoesNotExist, AmbigiousAtom, DepError) as e:
                if args.debug:
                    traceback.print_exc()
                error(f"{e}")
            except Exception as e:
                # Always print stack trace for Unknown exceptions
                traceback.print_exc()
                error(f"{e}")

    if args.sort_vfs:
        global_updates()

    display_unread_message()


def pybuild_validate(file_name):
    # Verify that pybuild is valid python
    import py_compile

    py_compile.compile(file_name, doraise=True)

    # Verify fields of pybuild
    mod = full_load_file(file_name)
    mod.validate()


def pybuild_manifest(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError(l10n("file-does-not-exist", file=file_name))

    repo_root = get_repo_root(file_name)

    if repo_root is None:
        raise FileNotFoundError(l10n("repository-does-not-exist"))

    # Register repo in case it's not already in repos.cfg
    REAL_ROOT = os.path.realpath(repo_root)
    if not any([REAL_ROOT == os.path.realpath(repo.location) for repo in env.REPOS]):
        sys.path.append(os.path.join(repo_root))
        env.REPOS.append(
            Repo(os.path.basename(repo_root), repo_root, False, None, None, 0)
        )

    if env.ALLOW_LOAD_ERROR:
        raise Exception("Cannot allow load errors when generating manifest!")

    mod = full_load_file(file_name)

    create_manifest(mod)
    info(l10n("created-manifest", atom=mod.ATOM))
