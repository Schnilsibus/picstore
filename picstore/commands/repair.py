from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Union
from picstore.core import PicDir, ParentDir
from picstore.config import config
from picstore.commands.list import List
from picstore.commands.view import View
from picstore.commands.command import Command


default_dir = Path(config.default_dir)


class Repair(Command):

    name = "repair"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("-dir",
                                help=f"path to the parent directory (or picdir) that needs repairing",
                                type=Path,
                                default=default_dir,
                                dest="directory")
        raw_parser.add_argument("--single",
                                help="indicate that 'dir' argument points to a picdir",
                                action="store_true",
                                default=False)

    @staticmethod
    def run(arguments: Namespace) -> None:
        Repair.repair(**vars(arguments))

    @staticmethod
    def repair(
            directory: Path,
            single: bool
    ) -> None:
        if not single:
            try:
                parent_picdir = ParentDir(directory=directory)
            except NotADirectoryError:
                print(f"ERROR: Cannot repair PicDirs in {directory} since its no directory")
                return
            if repair_all(parent_picdir=parent_picdir):
                print(f"repaired all picdirs in {directory}:")
            else:
                print(f"couldn't repair all picdirs in {directory}:")
            List.list(directory=directory, sort=None, reverse=False)
        else:
            repaired = _repair_single(directory=directory)
            if repaired is None or not repaired.is_intact():
                print(f"failed to repair {directory}")
            else:
                print(f"repaired {directory}:")
                View.view(directory=repaired.path.parent, name=repaired.name, date=repaired.date)


def repair_all(parent_picdir: ParentDir) -> bool:
    repaired_all = True
    for directory in parent_picdir.path.iterdir():
        if directory.is_dir():
            repaired = _repair_single(directory=directory)
            if repaired is None:
                repaired_all = False
            else:
                repaired_all = repaired_all and repaired.is_intact()
    return repaired_all


def _repair_single(directory: Path) -> Union[PicDir, None]:
    try:
        correct_name = PicDir.is_name_correct(directory=directory)
    except NotADirectoryError:
        print(f"ERROR: Cannot repair {directory} since is not a directory")
        return None
    if not correct_name:
        directory = PicDir.rename_directory(directory=directory)
        if not PicDir.is_name_correct(directory=directory):
            return None
    if not PicDir.required_directories_exist(directory=directory):
        PicDir.create_required_directories(directory=directory)
        if not PicDir.required_directories_exist(directory=directory):
            return None
    picdir = PicDir(path_or_parent=directory)
    picdir.add(directory=picdir.path)
    return picdir
