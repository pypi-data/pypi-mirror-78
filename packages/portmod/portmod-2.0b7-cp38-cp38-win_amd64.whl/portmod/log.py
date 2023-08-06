# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import logging
from .colour import bright, red, yellow
from .l10n import l10n


class PortmodFormatter(logging.Formatter):
    FORMATS = {
        logging.WARNING: logging.StrFormatStyle(
            bright(yellow("WARNING")) + ": {message}"
        ),
        logging.ERROR: logging.StrFormatStyle(bright(red("ERROR")) + ": {message}"),
        logging.CRITICAL: logging.StrFormatStyle(
            bright(red("CRITICAL")) + ": {message}"
        ),
        "DEFAULT": logging.StrFormatStyle("{message}"),
    }

    def __init__(self):
        super().__init__(style="{")

    def format(self, record):
        self._style = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        return logging.Formatter.format(self, record)


def init_logger(args):
    """Initializes python logger"""
    ch = logging.StreamHandler()
    if args.verbose:
        ch.setLevel(logging.DEBUG)
        logging.root.setLevel(logging.DEBUG)
    elif args.quiet:
        ch.setLevel(logging.WARN)
        logging.root.setLevel(logging.WARN)
    else:
        ch.setLevel(logging.INFO)
        logging.root.setLevel(logging.INFO)

    formatter = PortmodFormatter()
    ch.setFormatter(formatter)
    logging.root.addHandler(ch)


def add_logging_arguments(parser):
    parser.add_argument("-q", "--quiet", help=l10n("quiet-help"), action="store_true")
    parser.add_argument(
        "-v", "--verbose", help=l10n("verbose-help"), action="store_true"
    )
