from argparse import Namespace
import cli


# TODO: add it to github
# TODO: make separate projects for json_settings, pathlib_extended
# TODO: finish basic functionality (managing local FotoDirs)
# TODO: add syncing capabilities maybe make that a total separate application
# TODO: ONLY MAYBE add GUI


def main(args: Namespace):
    print(args)


if __name__ == "__main__":
    main(args=cli.parse())
