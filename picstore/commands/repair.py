from argparse import Namespace
from pathlib import Path
from shutil import move
from picstore.picdir import PicDir
from picstore.parentpicdir import ParentPicDir
from picstore.picowner import Ownership

# ROADMAP:
# - fix dir name (try to convert current name to valid one)
# - fix subdirs (all five there? if not create)
# - move files that are neither in RAW, STD, OTHR dir and have correct suffix e.g. one that is listed in config.json
# - move files that are wrongly in RAW or STD
# ---
# - make a system to repair whole parent dir
# - make a system to input ownership of the file by one of the following:
#   - once for whole parent_picdir (as cli arg)
#   - once for each pic dir (via cli input while running)
#   - for each file (via cli input while running)
#   - by the files metadata (IPTC) e.g. camera modell --> define my camera modells in config.json
#       --> use this library:  https://pypi.org/project/IPTCInfo3/
# - success


def repair_all(parent_picdir: ParentPicDir) -> bool:
    repaired_all = True
    for directory in parent_picdir.path.iterdir():
        repaired = repair(directory=directory)
        if repaired_all:
            repaired_all = repaired
    return repaired_all


def repair(directory: Path) -> bool:
    picdir = None
    if not PicDir.has_correct_name(directory=directory):
        directory = rename(directory=directory)
        if not PicDir.has_correct_name(directory=directory):
            return False
    if not PicDir.contains_sub_directories(directory=directory):
        picdir = create_subdirectories(directory=directory)
        if not PicDir.contains_sub_directories(directory=directory):
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
        owner: Ownership,

) -> bool:
    invalid_raw_files, invalid_std_files = picdir.wrong_files()
    top_level_files = tuple(picdir.path.iterdir())
    picdir.add_pictures(pictures=invalid_raw_files + invalid_std_files + top_level_files,
                        display_tqdm=display_tqdm,
                        picture_owner=owner,
                        use_cli=use_cli,
                        use_metadata=use_metadata,
                        copy=False)


def cli_repair(args: Namespace) -> None:
    if args.parent:
        repair_all(parent_picdir=ParentPicDir(directory=args.dir))
    else:
        repair(directory=args.dir)
