from picstore.app import run
from picstore.cli import parse


# TODO: error handling
# TODO: final look over everything (better type hints)
# TODO: final (manual) test of every command

def main():
    run(arguments=parse())


if __name__ == "__main__":
    main()
