from pathlib import Path
from datetime import date
from picdir import FotoDir
from argparse import ArgumentParser, Namespace


# TODO: write a ArgummentParser for the arguments of the create command
# TODO: code the create command (it creates a new FotoDir)

command_name = "create"
description = "creates a new foto dir"
epilog = "picstore create [...]"


class CreateParser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self,
                                prog=command_name,
                                description=description,
                                epilog=epilog)
        self.add_argument("name",
                          help="define the name")
        raise NotImplementedError()


def create(args: Namespace) -> FotoDir:
    return FotoDir(path_or_parent=args.parent_dir, name=args.name, start_date=args.start_date, source=args.source)