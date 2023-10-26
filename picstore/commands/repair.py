from argparse import ArgumentParser, Namespace
from pathlib import Path
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
    picdir = None
    if not PicDir.is_name_correct(directory=directory):
        directory = rename(directory=directory)
        if not PicDir.is_name_correct(directory=directory):
            return False
    if not PicDir.required_directories_exist(directory=directory):
        picdir = create_subdirectories(directory=directory)
        if not PicDir.required_directories_exist(directory=directory):
            return False
    if picdir is None:
        picdir = PicDir(path_or_parent=directory)
    move_files(picdir=picdir, owner=Ownership.Own)
    return picdir.is_intact()


def rename(directory: Path) -> Path:
    return PicDir.rename_directory(directory=directory)


def create_subdirectories(directory: Path) -> PicDir:
    return PicDir(path_or_parent=directory, create_dirs=True)


def move_files(
        picdir: PicDir,
        owner: Ownership = None,
        display_tqdm: bool = True,
        use_cli: bool = False,
        use_metadata: bool = True
) -> int:
    # TODO: handle files that were not moved (e.g. because their duplicates) --> delete?
    files = picdir.wrong_category_files(directory="RAW")
    files += picdir.wrong_category_files(directory="STD")
    files += picdir.wrong_category_files(directory="TOP")
    return picdir.add_pictures(pictures=tuple(files),
                               display_tqdm=display_tqdm,
                               picture_owner=owner,
                               use_cli=use_cli,
                               use_metadata=use_metadata,
                               copy=False)


def cli_repair(args: Namespace) -> None:
    print(args)
    if args.picdir:
        repair_single(directory=args.dir)
    else:
        repair_all(parent_picdir=ParentPicDir(directory=args.dir))
