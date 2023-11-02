from pathlib import Path
import datetime
from argparse import ArgumentParser, Namespace
from typing import Optional
from picstore.core import ParentDir, date_format
from picstore.config import config
from commands.command import Command
from commands import Add


default_dir = Path(config.default_dir)
sources = map(Path, config.default_sources)


class Create(Command):

    name = "create"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("name",
                                help="name of the new picdir")
        raw_parser.add_argument("-dir",
                                help=f"where to create the new picdir (default: {default_dir})",
                                type=Path,
                                default=default_dir,
                                dest="directory")
        raw_parser.add_argument("-d", "--date",
                                help="the date (YYYY-MM-DD) of the new picdir (default: today)",
                                type=lambda s: datetime.datetime.strptime(s, date_format),
                                default=datetime.date.today().strftime(date_format))
        raw_parser.add_argument("-s", "--source",
                                help="pictures to add in the new picdir \
                                     (still searches paths specified in config file if omitted)",
                                type=Path)
        raw_parser.add_argument("-b", "--bare",
                                help="make the new picdir empty",
                                action="store_true",
                                default=False)
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
        Create.create(**vars(arguments))

    @staticmethod
    def create(
            directory: Path,
            name: str,
            date: datetime.date,
            source: Optional[Path],
            bare: bool,
            recursive: bool,
            copy: bool
    ) -> None:
        picdir = ParentDir(directory=directory).add(name=name, date=date)
        print(f"created new picdir in {picdir.path}:\n{picdir}")
        if not bare:
            Add.run(arguments=Namespace(**locals()))
