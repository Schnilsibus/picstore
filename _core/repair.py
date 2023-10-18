from argparse import Namespace
from pathlib import Path
from picdir import PicDir, ParentPicDir, date_format
import datetime
import shutil

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
    if not PicDir.has_correct_name(directory=directory):
        successful = rename(directory=directory)
    if successful and not PicDir.contains_sub_directories(directory=directory):
        successful = create_subdirectories(directory=directory)
    if successful:
        picdir = PicDir(path_or_parent=directory)
        successful = move_files(picdir=picdir)
    return successful


def rename(directory: Path) -> bool:
    directory_name = directory.parts[-1]
    parts = directory_name.replace("-", "_").split("_")
    if len(parts) < 4:
        return False
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except ValueError:
        return False
    if 0 <= year <= 99:
        year += 2000
    if year < 2000 or month < 0 or month > 12 or day < 0 or day > 31:
        return False
    date = datetime.date(year=year, month=month, day=day)
    new_name = f"{date.strftime(date_format)}_{''.join(parts[3:])}"
    shutil.move(src=directory, dst=directory.parent / new_name)


def create_subdirectories(directory: Path) -> bool:
    picdir = PicDir(path_or_parent=directory, create_dirs=True)
    return PicDir.contains_sub_directories(directory)


def move_files(picdir: PicDir) -> bool:
    pass


def cli_repair(args: Namespace) -> None:
    pass
