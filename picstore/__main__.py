from picstore.app import run
from picstore.cli import parse


# TODO: errorhandling
# TODO: final look over everything (better type hints)
# TODO: final (manual) test of every command

def main():
    run(arguments=parse())


if __name__ == "__main__":
    main()
