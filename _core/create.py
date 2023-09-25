from pathlib import Path
import datetime
from picdir import PicDir
from argparse import Namespace


def create(directory: Path, name: str, date: datetime.date, source: Path) -> PicDir:
    newdir = PicDir(path_or_parent=directory, name=name, date=date, source=source)
    # TODO: do some output
    return newdir


def cli_create(args: Namespace) -> None:
    picdir = create(directory=args.dir, name=args.name, date=args.date, source=args.source)
