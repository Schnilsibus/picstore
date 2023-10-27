from picstore.app import run
from picstore.cli import parse


# TODO: try to add lightroom support
# TODO: add syncing capabilities maybe make that a total separate application


def main():
    run(arguments=parse())


if __name__ == "__main__":
    main()
