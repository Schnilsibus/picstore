from argparse import ArgumentParser, Namespace
from datetime import datetime
from typing import Collection, Optional
from pathlib import Path
from colorama import Style, Fore
from picstore.core.parentdir import ParentDir
from picstore.core.picdir import date_format
from picstore.config import config
from picstore.commands.command import Command

default_dir = Path(config.default_dir)


class View(Command):
    name = "view"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("name",
                                help="name of the picdir")
        raw_parser.add_argument("-dir",
                                help=f"dir in which all pic dirs should be listed (default: {default_dir})",
                                type=Path,
                                dest="directory",
                                default=default_dir)
        raw_parser.add_argument("-d", "--date",
                                help="the date (DD-MM-YY) of the picdir",
                                type=lambda s: datetime.strptime(s, date_format))

    @staticmethod
    def run(arguments: Namespace) -> None:
        View.view(**vars(arguments))

    @staticmethod
    def view(directory: Path, name: str, date: Optional[datetime.date] = None) -> None:
        parent_picdir = ParentDir(directory=directory)
        picdir = parent_picdir.get(name=name, date=date)
        if picdir is None:
            date_str = "" if date is None else f"with date {date.strftime(date_format)}"
            raise RuntimeError(f"picdir '{name}' {date_str} not found in {directory}")
        title = f"Information on PicDir '{picdir.name}':"
        print(f"{Style.BRIGHT}{title}{Style.RESET_ALL}" + "\n" + "-" * len(title))
        print(f"{'Name:'.ljust(10)}{picdir.name}")
        print(f"{'Date:'.ljust(10)}{picdir.date.strftime(date_format)}")
        print(f"{'#RAW:'.ljust(10)}{picdir.raw_count}")
        print(f"{'#STD:'.ljust(10)}{picdir.std_count}")
        print(f"{'Path:'.ljust(10)}{picdir.path}")
        if picdir.is_intact():
            print(f"{'Status:'.ljust(10)}{Fore.GREEN}ok{Style.RESET_ALL}")
        else:
            print(f"{'Status:'.ljust(10)}{Fore.RED}bad{Style.RESET_ALL}")
        print()
        print_files(title=f"Invalid in {picdir.raw.path}", files=picdir.raw.get_invalid_category_content())
        print_files(title=f"Invalid in {picdir.std.path}", files=picdir.std.get_invalid_owner_content())


def print_files(title: str, files: Collection[Path]) -> None:
    print(title)
    if len(files) > 0:
        print("\t" + "\n\t".join(map(lambda p: p.name, files)))
    else:
        print("\t---")
