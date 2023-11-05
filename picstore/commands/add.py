from pathlib import Path
from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Optional
from picstore.core import date_format, ParentDir, PicDirNotFoundError, PicDir
from picstore.commands.command import Command
from picstore.config import config


default_dir = Path(config.default_dir)
sources = map(Path, config.default_sources)


class Add(Command):

    name = "add"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("name",
                                help="name of the picdir")
        raw_parser.add_argument("-dir",
                                help=f"dir in which to search for the picdir (default: {default_dir})",
                                type=Path,
                                dest="directory",
                                default=default_dir)
        raw_parser.add_argument("-d", "--date",
                                help="the date (YYYY-MM-DD) of the picdir",
                                type=lambda s: datetime.strptime(s, date_format))
        raw_parser.add_argument("-s", "--source",
                                help="pictures to add in the new picdir \
                                      (still searches paths in config.json if omitted)",
                                type=Path)
        raw_parser.add_argument("-r", "--recursive",
                                help="try to add files at any depth in the source directory",
                                action="store_true",
                                default=False)
        raw_parser.add_argument("-c", "--copy",
                                help="specify to copy files (otherwise will move files)",
                                action="store_true",
                                default=False)

    @staticmethod
    def run(arguments: Namespace) -> None:
        Add.add(**vars(arguments))

    @staticmethod
    def add(
            directory: Path,
            name: str,
            date: Optional[datetime.date],
            source: Path,
            recursive: bool,
            copy: bool
    ) -> None:
        count = 0
        try:
            picdir = ParentDir(directory=directory).get(name=name, date=date)
        except NotADirectoryError as ex:
            print(f"ERROR: Cannot add to PicDirs in {directory} since its no directory")
            return
        except PicDirNotFoundError as ex:
            date_str = "" if date is None else date.strftime(date_format)
            print(f"ERROR: PicDir {name}, {date_str} not found in {directory}")
            return
        if source is not None:
            print(f"adding files from {source}")
            count = add_single_dir(picdir=picdir, source=source, recursive=recursive, copy=copy)
        else:
            for default_source in sources:
                print(f"adding files from {default_source}")
                count += add_single_dir(picdir=picdir, source=default_source, recursive=recursive, copy=copy)
        print(f"added {count} files to picdir in {picdir.path}:\n{picdir}")


def add_single_dir(picdir: PicDir, source: Path, recursive: bool, copy: bool) -> int:
    try:
        return picdir.add(directory=source, recursive=recursive, copy=copy)
    except NotADirectoryError:
        print(f"ERROR: Cannot add from {source} since its no directory")
        return 0
