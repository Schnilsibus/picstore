from argparse import ArgumentParser, Namespace
from pathlib import Path
from picstore.core.picdir import PicDir
from picstore.core.parentdir import ParentDir
from picstore.config import config
from picstore.commands.command import Command
from picstore.commands.list import List
from picstore.commands.view import View


default_dir = Path(config.default_dir)


class Repair(Command):

    name = "repair"

    def __init__(self):
        Command.__init__(self)

    @staticmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raw_parser.add_argument("-dir",
                                help=f"path to the parent directory (or picdir) \
                                       that needs repairing (default: {default_dir}).",
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
            parent_picdir = ParentDir(directory=directory)
            if repair_all(parent_picdir=parent_picdir):
                print(f"repaired all picdirs in {directory}:")
            else:
                print(f"couldn't repair all picdirs in {directory}:")
            List.list(directory=directory)
        else:
            if repair_single(directory=directory):
                print(f"repaired picdir in {directory}:")
                picdir = PicDir(path_or_parent=directory)
                View.view(directory=picdir.path.parent, name=picdir.name, date=picdir.date)
            else:
                print(f"failed to repair picdir in {directory}")


def repair_all(parent_picdir: ParentDir) -> bool:
    repaired_all = True
    for directory in parent_picdir.path.iterdir():
        if directory.is_dir():
            repaired = repair_single(directory=directory)
            repaired_all = repaired_all and repaired
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
    resort_files(picdir=picdir)
    return picdir.is_intact()


def resort_files(
        picdir: PicDir,
        display_tqdm: bool = True
) -> int:
    return picdir.add(directory=picdir.path,
                      display_tqdm=display_tqdm,
                      recursive=True,
                      copy=False)
