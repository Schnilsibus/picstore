from argparse import Namespace
from picstore.commands.list import List
from picstore.commands.view import View
from picstore.commands.create import Create
from picstore.commands.repair import Repair
from picstore.commands.add import Add

all_commands = [
    List(),
    View(),
    Create(),
    Repair(),
    Add()
]


def run(arguments: Namespace) -> None:
    command_to_run = vars(arguments).pop("command")
    for command in all_commands:
        if command_to_run == command.name:
            command.run(arguments=arguments)
            break
