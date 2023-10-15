from argparse import Namespace
import cli
from create import cli_create
from list import cli_list
from view import cli_view


# TODO: [make separate projects for pathlib_extended]
# TODO: add doc strings
# TODO: solution for default sources (and implement them) (maybe add --bare option to create that lets you specify that you definetly want a empty new picdir)
# TODO: add syncing capabilities maybe make that a total separate application


def main(args: Namespace):
    cmd = vars(args).pop("command")
    if cmd == "create":
        cli_create(args=args)
    elif cmd == "list":
        cli_list(args=args)
    elif cmd == "view":
        cli_view(args=args)


if __name__ == "__main__":
    main(args=cli.parse())
