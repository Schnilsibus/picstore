from argparse import Namespace
from picstore.commands.create import cli_create
from picstore.commands.list import cli_list
from picstore.commands.view import view
from picstore.commands.repair import cli_repair
import picstore.cli as cli


# TODO: add doc strings
# TODO: add repair command
# TODO: add add command
# TODO: add lightroom support
# TODO: change concept of commands only one main method --> construct parser so that you can call it as method(**args)
# TODO: add syncing capabilities maybe make that a total separate application


def main(args: Namespace):
    cmd = vars(args).pop("command")
    if cmd == "create":
        cli_create(args=args)
    elif cmd == "list":
        cli_list(args=args)
    elif cmd == "view":
        view(**vars(args))
    elif cmd == "repair":
        cli_repair(args=args)


if __name__ == "__main__":
    main(args=cli.parse())
