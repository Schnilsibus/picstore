from argparse import Namespace
from typing import Literal, Tuple
from pathlib import Path
from picstore.picdir import PicDir
from picstore.parentpicdir import ParentPicDir


# TODO: display more wrong files: wrong category also in top-level dir; wrong owners


def list_picdirs(directory: Path, sort: Literal["date", "name", "raw", "std"] = None) -> Tuple[PicDir]:
    picdirs = list(ParentPicDir(directory=directory))
    if sort == "raw":
        picdirs.sort(key=lambda d: d.num_raw_files)
    elif sort == "std":
        picdirs.sort(key=lambda d: d.num_std_files)
    elif sort == "name":
        picdirs.sort(key=lambda d: d.name)
    elif sort == "date":
        picdirs.sort(key=lambda d: d.date)
    return tuple(picdirs)


def cli_list(args: Namespace) -> None:
    picdirs = list_picdirs(directory=args.dir, sort=args.sort)
    print(PicDir.table_header())
    for picdir in picdirs:
        print(str(picdir))
