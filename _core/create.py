from pathlib import Path
from datetime import date, datetime
from picdir import PicDir
from argparse import ArgumentParser, Namespace


# TODO: write a ArgumentParser for the arguments of the create command
# TODO: code the create command (it creates a new FotoDir)

command_name = "create"
description = "creates a new picdir"
epilog = ""


class CreateParser(ArgumentParser):

    _DATE_FORMAT = "%d-%m-%y"

    def __init__(self, default_dir: Path):
        ArgumentParser.__init__(self,
                                prog=command_name,
                                description=description,
                                epilog=epilog)
        self.add_argument("name",
                          help="name of the new picdir")
        self.add_argument("-dir", "--parent-dir",
                          help=f"where to create the new picdir (default: {str(default_dir)}",
                          type=Path,
                          default=default_dir)
        self.add_argument("-d", "--date",
                          help="the date (DD-MM-YY) of the new picdir (default: today)",
                          type=lambda s: datetime.strptime(s, CreateParser._DATE_FORMAT),
                          default=date.today())
        self.add_argument("-s", "--source",
                          help="pictures to add in the new picdir",
                          type=Path)


def create(args: Namespace) -> PicDir:
    newdir = PicDir(path_or_parent=args.parent_dir, name=args.name, start_date=args.start_date, source=args.source)
    # TODO: do some output
    return newdir
