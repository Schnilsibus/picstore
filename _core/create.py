from pathlib import Path
import datetime
from picdir import PicDir
from argparse import Namespace


def create(directory: Path, name: str, date: datetime.date, source: Path) -> PicDir:
    return PicDir(path_or_parent=directory, name=name, date=date, source=source)


def cli_create(args: Namespace) -> None:
    print(f"creating new picdir in {str(args.dir)}")
    new_picdir = create(directory=args.dir, name=args.name, date=args.date, source=args.source)
    print(f"created new picdir in {str(new_picdir.path)}:")
    print(str(new_picdir))
