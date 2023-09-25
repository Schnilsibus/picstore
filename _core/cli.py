from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import Callable
from pathlib import Path
from datetime import datetime, date


# TODO: replace _default_dir with setting


program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = ""

_DATE_FORMAT = "%d-%m-%y"

_default_dir = Path(r"C:\Users\Nils\Pictures\mypics")


class PicParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self,
                                prog=program_name,
                                description=description,
                                epilog=epilog)


class CommandParser(ArgumentParser):
    def __init__(self, parser_factory: Callable, **kwargs):
        ArgumentParser.__init__(self, **kwargs)
        parser_factory(self)


def create_parser_factory(parser: ArgumentParser) -> None:
    parser.add_argument("name",
                        help="name of the new picdir")
    parser.add_argument("-dir", "--parent-dir",
                        help=f"where to create the new picdir",
                        type=Path,
                        default=str(_default_dir),
                        dest="dir")
    parser.add_argument("-d", "--date",
                        help="the date (DD-MM-YY) of the new picdir",
                        type=lambda s: datetime.strptime(s, _DATE_FORMAT),
                        default=date.today().strftime(_DATE_FORMAT))
    parser.add_argument("-s", "--source",
                        help="pictures to add in the new picdir",
                        type=Path)


def list_parser_factory(parser: ArgumentParser) -> None:
    parser.add_argument("-dir",
                        help=f"dir in which all pic dirs should be listed (default: {str(_default_dir)})",
                        type=Path,
                        default=_default_dir)
    parser.add_argument("-s", "--sort",
                        help="sort the output",
                        choices=["date", "name", "raw", "std"])


def construct_parser() -> PicParser:
    parser = PicParser()
    subparsers_action = parser.add_subparsers(title="commands",
                                              description="a subparsers group description",
                                              parser_class=CommandParser,
                                              dest="command")
    subparsers_action.add_parser(name="create",
                                 parser_factory=create_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="list",
                                 parser_factory=list_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


def parse() -> Namespace:
    return construct_parser().parse_args()


if __name__ == "__main__":
    parse()
