from argparse import Namespace
from picstore.commands.list import list_picdirs
from picstore.commands.view import view


def run(arguments: Namespace) -> None:
    command = vars(arguments).pop("command")
    if command == "create":
        pass
    elif command == "list":
        list_picdirs(*vars(arguments))
    elif command == "view":
        view(**vars(arguments))
    elif command == "repair":
        pass
