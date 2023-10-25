from argparse import ArgumentParser
from typing import Literal
from pathlib import Path
from app.core.picdir import PicDir
from app.core.parentpicdir import ParentPicDir
from app.config import config


default_dir = config.default_dir


def list_parser_factory(parser: ArgumentParser) -> None:
    parser.add_argument("-dir",
                        help=f"dir in which all pic dirs should be listed (default: {default_dir})",
                        type=Path,
                        default=default_dir)
    parser.add_argument("-s", "--sort",
                        help="sort the output",
                        choices=["date", "name", "raw", "std"])
    parser.add_argument("-r", "--reverse",
                        help="reverse the list",
                        action="store_true",
                        default=False)


def list_picdirs(directory: Path, sort: Literal["date", "name", "raw", "std"] = None, reverse: bool = False) -> None:
    picdirs = ParentPicDir(directory=directory).sort(attribute=sort)
    if reverse:
        picdirs = reversed(picdirs)
    print(PicDir.table_header())
    for picdir in picdirs:
        print(picdir)
