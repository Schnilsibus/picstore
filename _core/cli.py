from argparse import ArgumentParser, Namespace
from typing import Callable


program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = ""


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


def parse() -> Namespace:
    parser = PicParser()
    subparsers_action = parser.add_subparsers(title="commands",
                                              description="a subparsers group description",
                                              parser_class=CommandParser)
    subparsers_action.add_parser(name="help", parser_factory=help_parser_factory)
    subparsers_action.add_parser(name="create", parser_factory=create_parser_factory)
    subparsers_action.add_parser(name="list", parser_factory=list_parser_factory)
    return parser.parse_args()


if __name__ == "__main__":
    parse()
