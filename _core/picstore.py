from argparse import Namespace
import cli
from create import cli_create
from list import cli_list


# TODO: [make separate projects for pathlib_extended]
# TODO: add doc strings
# TODO: add view command --> detailed view of one pic dir if status is not okay shows why
# TODO: solution for names (should they be unique if not how can you choose the exact picdir you want?)
# TODO: add syncing capabilities maybe make that a total separate application


def main(args: Namespace):
    cmd = vars(args).pop("command")
    if cmd == "create":
        cli_create(args=args)
    elif cmd == "list":
        cli_list(args=args)


if __name__ == "__main__":
    main(args=cli.parse())
