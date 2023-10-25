from picstore.app import run
import picstore.cli as cli


# TODO: add doc strings
# TODO: add repair command
# TODO: add add command
# TODO: add lightroom support
# TODO: change concept of commands only one main method --> construct parser so that you can call it as method(**args)
# TODO: think about giving each sub dir a py representation class --> better code structure
# TODO: add syncing capabilities maybe make that a total separate application


def main():
    run(arguments=cli.parse())


if __name__ == "__main__":
    main()
