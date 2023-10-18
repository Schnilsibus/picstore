from argparse import Namespace
import cli
from create import cli_create
from list import cli_list
from view import cli_view
from repair import cli_repair


# TODO: [make separate projects for pathlib_extended]
# TODO: add doc strings
# TODO: add repair command
# TODO: maybe add check in picdir that checks if all files in RAW/STD are mine and all in OTHER are not mine (by looking at IPTC data and config.json)
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
