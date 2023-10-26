from argparse import ArgumentParser, Namespace
from typing import Literal, Optional
from pathlib import Path
from picstore.core.picdir import PicDir
from picstore.core.parentpicdir import ParentPicDir
from picstore.config import config
from picstore.commands.command import Command

default_dir = Path(config.default_dir)


class List(Command):

    name = "list"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("-dir",
                                help=f"dir in which all pic dirs should be listed (default: {default_dir})",
                                type=Path,
                                dest="directory",
                                default=default_dir)
        raw_parser.add_argument("-s", "--sort",
                                help="sort the output",
                                choices=["date", "name", "raw", "std"])
        raw_parser.add_argument("-r", "--reverse",
                                help="reverse the list",
                                action="store_true",
                                default=False)

    @staticmethod
    def run(arguments: Namespace) -> None:
        List.list(**vars(arguments))

    @staticmethod
    def list(
            directory: Path,
            sort: Optional[Literal["date", "name", "raw", "std"]] = None,
            reverse: bool = False
    ) -> None:
        picdirs = ParentPicDir(directory=directory)
        if sort is not None:
            picdirs.sort(attribute=sort)
        if reverse:
            picdirs = reversed(picdirs)
        print(PicDir.table_header())
        for picdir in picdirs:
            print(picdir)
