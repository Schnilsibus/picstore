from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import Callable
from picstore.commands.list import List
from picstore.commands.view import View
from picstore.commands.create import Create
from picstore.commands.repair import Repair
from picstore.commands.add import Add


program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. \
               It's core functionality is to organize pictures in 'picdirs'."
epilog = "'picstore <command> -h' for detailed information on a command."
all_commands = [
    List,
    View,
    Create,
    Repair,
    Add
]


class PicParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self,
                                prog=program_name,
                                description=description,
                                epilog=epilog)


class CommandParser(ArgumentParser):
    def __init__(self, parser_factory: Callable[[ArgumentParser, ], None], **kwargs):
        ArgumentParser.__init__(self, **kwargs)
        parser_factory(self)


def construct_parser() -> PicParser:
    parser = PicParser()
    subparsers_action = parser.add_subparsers(title="commands",
                                              parser_class=CommandParser,
                                              dest="command")
    for command in all_commands:
        subparsers_action.add_parser(name=command.name,
                                     parser_factory=command.construct_parser,
                                     formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


def parse() -> Namespace:
    return construct_parser().parse_args()
