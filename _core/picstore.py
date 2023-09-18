from argparse import ArgumentParser, Namespace
from create import create, CreateParser


# TODO: add it to github
# TODO: make separate projects for json_settings, pathlib_extended
# TODO: finish basic functionality (managing local FotoDirs)
# TODO: add syncing capabilities maybe make that a total separate application
# TODO: ONLY MAYBE add GUI

program_name = "picstore"
description = "picstore is a cmd program that handles storage of pictures. " \
              "It's core functionality is to organize pictures in different directories."
epilog = ""


class PicParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self,
                                prog=program_name,
                                description=description,
                                epilog=epilog)
        self.add_argument("command",
                          help="choose a command for picstore to execute")
        self.add_argument("cmdargs",
                          nargs="*",
                          help="arguments for the chosen command")


def main(args: Namespace):
    if args.command == "help":
        print("help")
    elif args.command == "list":
        print("list")
    elif args.command == "create":
        print(f"{', '.join(args.args)}")


if __name__ == "__main__":
    main(args=PicParser().parse_args())
