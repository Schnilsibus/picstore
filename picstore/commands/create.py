from pathlib import Path
import datetime
from argparse import Namespace
from typing import Union, List
from core.picdir import PicDir
from core.parentpicdir import ParentPicDir
from app.config import config


_sources = map(Path, config.sources)


def create(directory: Path, name: str, date: datetime.date, source: Union[Path, List[Path]] = None) -> PicDir:
    return ParentPicDir(directory=directory).add(name=name, date=date, source=source)


def cli_create(args: Namespace) -> None:
    print(f"creating new picdir in {str(args.dir)}")
    try:
        if args.bare:
            new_picdir = create(directory=args.dir, name=args.name, date=args.date)
        elif args.source is not None:
            new_picdir = create(directory=args.dir, name=args.name, date=args.date, source=args.source)
        else:
            files = []
            for source in _sources:
                if source.is_dir():
                    files.extend(source.iterdir())
            new_picdir = create(directory=args.dir, name=args.name, date=args.date, source=files)
    except BaseException as ex:
        print(ex)
        return
    print(f"created new picdir in {str(new_picdir._path)}:")
    print(str(new_picdir))
