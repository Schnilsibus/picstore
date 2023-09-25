from argparse import Namespace
from typing import Literal, Tuple
from picdir import PicDir
from pathlib import Path


# TODO: write ArgumentParser for args of list command
# TODO: code list command (it lists all FotoDirs in a dir)


Attribute = Literal["date", "name", "raw", "std"]


def list_pic_dirs(directory: Path, sort: Attribute = None) -> Tuple[PicDir]:
    subdirs = filter(lambda p: p.is_dir(), directory.iterdir())
    picdirs = map(lambda d: PicDir(path_or_parent=d), subdirs)
    if sort is not None:
        picdirs = sorted(picdirs, key=lambda d: d.__dict__[sort])
    return tuple(picdirs)


def cli_list(args: Namespace) -> None:
    picdirs = list_pic_dirs(directory=args.dir, sort=args.sort)
    for picdir in picdirs:
        print(str(picdir))
