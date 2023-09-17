from argparse import ArgumentParser, Namespace
from typing import List


# TODO: add documentation

program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = ""


class PicParser(ArgumentParser):
    def __init__(self, commands: List[str]):
        ArgumentParser.__init__(self,
                                prog=program_name,
                                description=description,
                                epilog=epilog)
        self.add_argument("command",
                          choices=commands,
                          help="choose a command for picstore to execute")
        self.add_argument("args",
                          nargs="*",
                          help="arguments for the chosen command")


def parse_arguments(commands: List[str]) -> Namespace:
    parser = PicParser(commands=commands)
    return parser.parse_args()
