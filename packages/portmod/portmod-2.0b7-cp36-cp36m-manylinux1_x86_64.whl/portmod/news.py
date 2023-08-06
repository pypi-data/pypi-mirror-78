# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Critical News module

See https://www.gentoo.org/glep/glep-0042.html for details

We use yaml instead of txt for ease of parsing, while having almost the same structure
Note that a Body field is used for the article body.
"""

import os
from fnmatch import fnmatch
from glob import glob
from typing import Callable, Optional

from portmod.portmod import parse_news
from .colour import blue, bright, green, yellow
from .config import get_config
from .globals import env
from .repo.list import read_list
from .repo.loader import load_installed_mod
from .repo.profiles import get_profile_path, profile_exists
from .repo import Atom
from .repos import Repo
from .l10n import l10n, get_locales


def get_article_path(repo_root: str, article: str) -> Optional[str]:
    path = os.path.join(repo_root, "metadata", "news", article)
    for locale in get_locales():
        article_path = os.path.join(path, article + "." + locale + ".yaml")
        if os.path.exists(article_path):
            return article_path
    return None


def is_news_visible(repo: Repo, article: str) -> bool:
    """
    Returns true if the given news article is visible to the user.
    """
    article = parse_news(get_article_path(repo.location, article))

    def get_list(ob, key):
        if isinstance(ob, list):
            li = ob
        elif isinstance(ob, str):
            li = ob.split()
        else:
            raise TypeError(
                f"{key} should contain a string or a list, " f"but contained {ob}"
            )
        return li

    installed_conditions = get_list(
        article.display_if_installed or "", "Display-If-Installed"
    )
    keyword_conditions = get_list(
        article.display_if_keyword or "", "Display-If-Keyword"
    )
    profile_conditions = get_list(
        article.display_if_profile or "", "Display-If-Profile"
    )

    profile_name = os.path.relpath(
        get_profile_path(), os.path.join(repo.location, "profiles")
    )
    if profile_conditions and not any(
        fnmatch(profile_name, profile_condition)
        for profile_condition in profile_conditions
    ):
        return False

    if installed_conditions and not any(
        load_installed_mod(Atom(atom)) for atom in installed_conditions
    ):
        return False

    ACCEPT_KEYWORDS = set(get_config()["ACCEPT_KEYWORDS"])
    if keyword_conditions and not any(
        keyword in ACCEPT_KEYWORDS or keyword.lstrip("~") in ACCEPT_KEYWORDS
        for keyword in keyword_conditions
    ):
        return False

    return True


def is_news_unread(repo: Repo, article: str) -> bool:
    """
    Returns true if the given news article needs to be read.
    """
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
    if not os.path.exists(unread_file) or article in read_list(unread_file):
        return True

    return False


def mark(repo: Repo, article: str, read=True):
    """Marks the given news article as read"""
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    os.makedirs(news_dir, exist_ok=True)
    if read:
        remove_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        add_file = os.path.join(news_dir, "news-" + repo.name + ".read")
    else:
        add_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        remove_file = os.path.join(news_dir, "news-" + repo.name + ".read")

    if os.path.exists(remove_file):
        contents = read_list(remove_file)

        if article in contents:
            del contents[contents.index(article)]
            with open(remove_file, "w") as file:
                for line in contents:
                    print(line + "\n", file=file)
        else:
            return

    with open(add_file, "a") as file:
        print(article, file=file)


def iterate_news(repo: Repo, unread_only=False, visible_only=False):
    news_dir = os.path.join(repo.location, "metadata", "news")
    unread_file = os.path.join(
        os.path.join(env.PORTMOD_LOCAL_DIR, "news"), "news-" + repo.name + ".unread"
    )
    if os.path.exists(unread_file):
        unread = set(read_list(unread_file))
    else:
        unread = set()

    if os.path.exists(news_dir):
        for news_item in sorted(os.listdir(news_dir)):
            if (not unread_only or news_item in unread) and (
                not visible_only or is_news_visible(repo, news_item)
            ):
                yield os.path.join(news_dir, news_item)


def display_unread_message():
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    total_unread = 0
    for repo in env.REPOS:
        unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        if os.path.exists(unread_file):
            unread = len(read_list(unread_file))
            if unread:
                if not total_unread:
                    print()
                print(
                    bright(yellow(" * " + l10n("important")))
                    + l10n("news-unread", unread=unread, repo=repo.name)
                )
            total_unread += unread

    if total_unread:
        print(
            bright(yellow(" * "))
            + l10n("news-read", command=bright(green("omwselect news read")))
        )
        print()


def update_news():
    news_dir = os.path.join(env.PORTMOD_LOCAL_DIR, "news")
    os.makedirs(news_dir, exist_ok=True)
    for repo in env.REPOS:
        unread_file = os.path.join(news_dir, "news-" + repo.name + ".unread")
        skip_file = os.path.join(news_dir, "news-" + repo.name + ".skip")
        if os.path.exists(skip_file):
            skip = set(read_list(skip_file))
        else:
            skip = set()

        for news_dir in iterate_news(repo):
            news_item = os.path.basename(news_dir)
            if news_item in skip:
                continue

            if (
                profile_exists()
                and is_news_visible(repo, news_item)
                and os.path.exists(unread_file)
            ):
                with open(unread_file, "a") as file:
                    print(news_item, file=file)

            with open(skip_file, "a+") as file:
                print(news_item, file=file)

        if not os.path.exists(unread_file):
            # If unread file doesn't exist, this must be a newly added repository
            # In this case, all enws is old news, so it gets added to the skip file
            # above, but not to the unread file
            with open(unread_file, "w") as file:
                file.write("")

    return True


def read_news(index=None, unread_only=False):
    i = 0
    for repo in env.REPOS:
        for news_dir in iterate_news(repo, unread_only=unread_only):
            if index is not None and i < index:
                i += 1
                continue
            elif index is not None and i > index:
                break

            news_item = os.path.basename(news_dir)
            article = parse_news(get_article_path(repo.location, news_item))

            max_len = max(
                len(article.title),
                len(article.author),
                len(article.translator or ""),
                len(article.posted),
                len(article.revision),
            )
            print(bright(green((news_item))))
            print("  " + l10n("title").ljust(max_len) + article.title)
            print("  " + l10n("author").ljust(max_len) + article.author)
            if article.translator:
                print("  " + l10n("translator").ljust(max_len) + article.translator)
            print("  " + l10n("posted").ljust(max_len) + article.posted)
            print("  " + l10n("revision").ljust(max_len) + article.revision)
            print()
            print(article.body)
            print()

            mark(repo, news_item)
            i += 1


def add_news_parsers(subparsers):
    news = subparsers.add_parser("news", help=l10n("news-help"))
    news_subparsers = news.add_subparsers()
    news_list = news_subparsers.add_parser("list", help=l10n("news-list-help"))
    news_read = news_subparsers.add_parser("read", help=l10n("news-read-help"))
    news_read.add_argument(
        "target",
        help=l10n("news-read-target-help"),
        default=l10n("news-read-target-new"),
        metavar="<" + l10n("news-target-placeholder") + ">",
        nargs="?",
    )
    news_unread = news_subparsers.add_parser("unread", help=l10n("news-unread-help"))
    news_unread.add_argument(
        "target",
        help=l10n("news-unread-target-help"),
        metavar="<" + l10n("news-target-placeholder") + ">",
    )

    def read_func(args):
        if args.target == l10n("news-read-target-new"):
            read_news(unread_only=True)
        elif args.target == l10n("news-read-target-all"):
            read_news()
        else:
            read_news(int(args.target))

    def list_func(args):
        i = 0
        print(bright(green(l10n("news-items"))))
        for repo in env.REPOS:
            for path in iterate_news(repo):
                article_name = os.path.basename(path)
                article = parse_news(get_article_path(repo.location, article_name))
                if is_news_unread(repo, article_name):
                    print(
                        f'  {bright("[" + str(i) + "]")}  {blue("N")}  '
                        f"{article.posted}  {blue(article.title)}"
                    )
                else:
                    print(
                        f'  {bright("[" + str(i) + "]")}     '
                        f"{article.posted}  {article.title}"
                    )
                i += 1

    def news_help(args):
        news.print_help()

    def unread_func(args):
        i = 0
        for repo in env.REPOS:
            for path in iterate_news(repo):
                if args.target == "all" or i == int(args.target):
                    article_name = os.path.basename(path)
                    mark(repo, article_name, read=False)
                i += 1

    news.set_defaults(func=news_help)
    news_read.set_defaults(func=read_func)
    news_list.set_defaults(func=list_func)
    news_unread.set_defaults(func=unread_func)


def validate_news(repo_root: str, err: Callable[[str], None]):
    """Validates the news files in the given repository"""
    path = os.path.join(repo_root, "metadata", "news")
    if os.path.exists(path):
        for directory in os.listdir(path):
            files = glob(os.path.join(path, directory, directory + ".*.yaml"))
            for news_file in files:
                article = parse_news(news_file)

                if article.display_if_installed:
                    string = article.display_if_installed
                    for atom in string.split():
                        Atom(atom)
            if not files:
                err(
                    f"News directory {path}/{directory} doesn't contain any files of "
                    f"the form {directory}.*.yaml"
                )
