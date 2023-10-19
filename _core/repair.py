from argparse import Namespace
from pathlib import Path
from picdir import PicDir, ParentPicDir
from picowner import Ownership

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
    pass


def repair(directory: Path) -> bool:
    successful = True
    new_directory = None
    picdir = None
    if not PicDir.has_correct_name(directory=directory):
        new_directory = rename(directory=directory)
        successful = PicDir.has_correct_name(directory=new_directory)
    if successful and not PicDir.contains_sub_directories(directory=new_directory):
        picdir = create_subdirectories(directory=directory)
        successful = PicDir.contains_sub_directories(directory=picdir.path)
    if successful:
        successful = move_files(picdir=picdir)
    return successful


def rename(directory: Path) -> Path:
    return PicDir.correct_directory_name(directory=directory)


def create_subdirectories(directory: Path) -> PicDir:
    return PicDir(path_or_parent=directory, create_dirs=True)


def move_files(
        picdir: PicDir,
        owner: Ownership = Ownership.Undefined,
        cli_input_file_by_file: bool = False,
        use_meta_data: bool = True
) -> bool:
    pass


def cli_repair(args: Namespace) -> None:
    pass
