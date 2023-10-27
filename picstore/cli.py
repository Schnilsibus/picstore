from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import Callable
from picstore.commands.list import List
from picstore.commands.view import View
from picstore.commands.create import Create
from picstore.commands.repair import Repair
from picstore.commands.add import Add


program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = "'picstore <command> -h' for detailed information on a command."


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


def construct_parser() -> PicParser:
    parser = PicParser()
    subparsers_action = parser.add_subparsers(title="commands",
                                              parser_class=CommandParser,
                                              dest="command")
    subparsers_action.add_parser(name="list",
                                 parser_factory=List.construct_parser,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="view",
                                 parser_factory=View.construct_parser,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="create",
                                 parser_factory=Create.construct_parser,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="repair",
                                 parser_factory=Repair.construct_parser,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers_action.add_parser(name="add",
                                 parser_factory=Add.construct_parser,
                                 formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


def parse() -> Namespace:
    return construct_parser().parse_args()


if __name__ == "__main__":
    parse()
