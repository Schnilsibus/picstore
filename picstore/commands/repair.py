from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional
from picstore.core.picdir import PicDir
from picstore.core.parentpicdir import ParentPicDir
from picstore.core.picowner import Ownership
from picstore.config import config
from picstore.commands.command import Command

default_dir = Path(config.default_dir)


class Repair(Command):
    name = "repair"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("-dir",
                                help=f"path to the (parent) picdir that needs repairing (default: {default_dir}).",
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
        print("repair")
        if not single:
            parent_picdir = ParentPicDir(directory=directory)
            repair_all(parent_picdir=parent_picdir)
        else:
            repair_single(directory=directory)


def repair_all(parent_picdir: ParentPicDir) -> bool:
    repaired_all = True
    for directory in parent_picdir.path.iterdir():
        repaired = repair_single(directory=directory)
        if repaired_all:
            repaired_all = repaired
    return repaired_all


def repair_single(directory: Path) -> bool:
    if not PicDir.is_name_correct(directory=directory):
        directory = PicDir.rename_directory(directory=directory)
        if not PicDir.is_name_correct(directory=directory):
            return False
    if not PicDir.required_directories_exist(directory=directory):
        PicDir.create_required_directories(directory=directory)
        if not PicDir.required_directories_exist(directory=directory):
            return False
    picdir = PicDir(path_or_parent=directory)
    move_files(picdir=picdir)
    return picdir.is_intact()


def move_files(
        picdir: PicDir,
        display_tqdm: bool = True,
        use_shell: bool = True
) -> int:
    return picdir.add(directory=picdir.path,
                      display_tqdm=display_tqdm,
                      use_shell=use_shell,
                      recursive=True,
                      copy=False)



