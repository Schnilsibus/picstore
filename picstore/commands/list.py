from argparse import Namespace
from typing import Literal, Tuple
from pathlib import Path
from picstore.picdir import PicDir
from picstore.parentpicdir import ParentPicDir


def list_picdirs(directory: Path, sort: Literal["date", "name", "raw", "std"] = None) -> Tuple[PicDir]:
    picdirs = list(ParentPicDir(directory=directory))
    if sort is not None:
        picdirs.sort(key=lambda d: vars(d)[sort])
    return tuple(picdirs)


def cli_list(args: Namespace) -> None:
    picdirs = list_picdirs(directory=args.dir, sort=args.sort)
    print(PicDir.table_header())
    for picdir in picdirs:
        print(str(picdir))
