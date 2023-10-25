from argparse import Namespace
from pathlib import Path
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
#   - by the files metadata (IPTC) e.g. camera model --> define my camera modells in config.json
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
        repair(directory=args.dir)
    else:
        repair_all(parent_picdir=ParentPicDir(directory=args.dir))