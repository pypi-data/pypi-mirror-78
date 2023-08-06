# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
CLI for interacting with the user's use flag configuration
"""

import sys
import argparse
import traceback
from logging import error
from typing import Optional
from .log import init_logger, add_logging_arguments
from .globals import env
from .repo.use import add_use, remove_use, InvalidFlag
from .repo import Atom
from .l10n import l10n


def main():
    """
    Main function for the omwuse executable
    """
    parser = argparse.ArgumentParser(description=l10n("use-help"))
    parser.add_argument("-E", metavar="USE", help=l10n("use-enable"))
    parser.add_argument("-D", metavar="USE", help=l10n("use-disable"))
    parser.add_argument("-R", metavar="USE", help=l10n("use-remove"))
    parser.add_argument("-m", metavar="MOD", help=l10n("use-package"))
    parser.add_argument("--debug", help=l10n("debug-help"), action="store_true")
    add_logging_arguments(parser)
    args = parser.parse_args()

    init_logger(args)

    if len(sys.argv) == 1:
        parser.print_help()

    if args.debug:
        env.DEBUG = True
    try:
        atom: Optional[Atom]
        if args.m is not None:
            atom = Atom(args.m)
        else:
            atom = None

        if args.E or args.D:
            if args.E:
                add_use(args.E, atom)
            elif args.D:
                add_use(args.D, atom, True)

        if args.R:
            remove_use(args.R, atom)
    except InvalidFlag as e:
        if env.DEBUG:
            traceback.print_exc()
        error(f"{e}")
    except Exception as e:
        traceback.print_exc()
        error(f"{e}")
