from argparse import Namespace
import cli
from create import cli_create
from list import cli_list


# TODO: add it to github
# TODO: make separate projects for json_settings, pathlib_extended
# TODO: finish basic functionality (managing local FotoDirs)
# TODO: add syncing capabilities maybe make that a total separate application
# TODO: ONLY MAYBE add GUI


def main(args: Namespace):
    cmd = vars(args).pop("command")
    if cmd == "create":
        cli_create(args=args)
    elif cmd == "list":
        cli_list(args=args)


if __name__ == "__main__":
    main(args=cli.parse())
