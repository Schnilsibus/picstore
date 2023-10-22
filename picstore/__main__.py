from argparse import Namespace
from picstore.commands.create import cli_create
from picstore.commands.list import cli_list
from picstore.commands.view import cli_view
from picstore.commands.repair import cli_repair
import cli


# TODO: [make separate projects for pathlib_extended]
# TODO: add doc strings
# TODO: add repair command
# TODO: maybe add check in picdir that checks if all files in RAW/STD are mine and all in OTHER are not mine (by looking at IPTC and EXIF? data and config.json)
# TODO: add syncing capabilities maybe make that a total separate application


def main(args: Namespace):
    cmd = vars(args).pop("command")
    if cmd == "create":
        cli_create(args=args)
    elif cmd == "list":
        cli_list(args=args)
    elif cmd == "view":
        cli_view(args=args)
    elif cmd == "repair":
        cli_repair(args=args)


if __name__ == "__main__":
    main(args=cli.parse())
