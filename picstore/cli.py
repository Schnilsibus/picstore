from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import Callable
from pathlib import Path
from datetime import datetime, date
from app.config import config


# TODO: move factory methods to commands -> maybe have abstractmethod (in a abstract class if needed) for noiceness


program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = "'picstore <command> -h' for detailed information for a command."

date_format = "%d-%m-%y"

_default_dir = config.default_dir


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
                        default=_default_dir,
                        dest="dir")
    parser.add_argument("-d", "--date",
                        help="the date (DD-MM-YY) of the new picdir",
                        type=lambda s: datetime.strptime(s, date_format),
                        default=date.today().strftime(date_format))
    parser.add_argument("-s", "--source",
                        help="pictures to add in the new picdir",
                        type=Path)
    parser.add_argument("-b", "--bare",
                        help="make the new picdir empty",
                        action="store_true")


def view_parser_factory(parser: ArgumentParser) -> None:
    parser.add_argument("name",
                        help="name of the picdir")
    parser.add_argument("-dir",
                        help=f"dir in which all pic dirs should be listed (default: {str(_default_dir)})",
                        type=Path,
                        dest="directory",
                        default=_default_dir)
    parser.add_argument("-d", "--date",
                        help="the date (DD-MM-YY) of the picdir",
                        type=lambda s: datetime.strptime(s, date_format))


def repair_parser_factory(parser: ArgumentParser) -> None:
    parser.add_argument("dir",
                        help="path to the (parent) picdir that needs repairing.",
                        type=Path,
                        default=_default_dir)
    parser.add_argument("--picdir",
                        help="indicate that 'dir' argument points to a picdir",
                        action="store_true")


def construct_parser() -> PicParser:
    parser = PicParser()
    subparsers_action = parser.add_subparsers(title="commands",
                                              parser_class=CommandParser,
                                              dest="command")
    subparsers_action.add_parser(name="create",
                                 parser_factory=create_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="list",
                                 parser_factory=list_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="view",
                                 parser_factory=view_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="repair",
                                 parser_factory=repair_parser_factory,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


def parse() -> Namespace:
    return construct_parser().parse_args()


if __name__ == "__main__":
    parse()
