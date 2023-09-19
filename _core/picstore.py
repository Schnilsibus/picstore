from argparse import ArgumentParser, Namespace
from create import create, CreateParser
from typing import Tuple


# TODO: add it to github
# TODO: make separate projects for json_settings, pathlib_extended
# TODO: finish basic functionality (managing local FotoDirs)
# TODO: add syncing capabilities maybe make that a total separate application
# TODO: ONLY MAYBE add GUI




def main(args: Namespace):
    if args.command == "help":
        print("help")
    elif args.command == "list":
        print("list")
    elif args.command == "create":
        print(f"{', '.join(args.args)}")


if __name__ == "__main__":
    main(args=PicParser().parse_args())
