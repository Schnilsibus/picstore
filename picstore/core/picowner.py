import enum
from pathlib import Path
from exiftool import ExifToolHelper
from typing import Tuple, Dict
from picstore.config import config


_my_camera_models = config.my_camera_models


class Ownership(enum.Enum):
    Own = enum.auto()
    Other = enum.auto()
    Undefined = enum.auto()


def owner(file_or_dir: Path, use_metadata: bool = True, use_shell: bool = True) -> Ownership:
    picture_owner = Ownership.Undefined
    if use_metadata:
        picture_owner = evaluate_owner(file=file_or_dir)
    if picture_owner == Ownership.Undefined and use_shell:
        picture_owner = ask_owner(file_or_dir=file_or_dir)
    return picture_owner


def owners(files_or_dirs: Tuple[Path], use_metadata: bool = True, use_shell: bool = True) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in files_or_dirs:
        picture_owners[picture] = owner(file_or_dir=picture, use_metadata=use_metadata, use_shell=use_shell)
    return picture_owners


def evaluate_owner(file: Path) -> Ownership:
    if not file.is_file():
        return Ownership.Undefined
    model_tag = "EXIF:Model"
    with ExifToolHelper() as et:
        metadata = et.get_metadata(str(file))[0]
        if model_tag in metadata:
            return Ownership.Own if metadata[model_tag] in _my_camera_models else Ownership.Other
        else:
            return Ownership.Undefined


def evaluate_owners(files: Tuple[Path]) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in files:
        picture_owners[picture] = evaluate_owner(file=picture)
    return picture_owners


def ask_owner(file_or_dir: Path) -> Ownership:
    while True:
        picture_owner = input(f"please select ownership for item {file_or_dir} ['OWN' / 'OTHR']: ").upper()
        if picture_owner == "OWN":
            return Ownership.Own
        elif picture_owner == "OTHR":
            return Ownership.Other
        else:
            print(f"\t -> {picture_owner} is not a valid input. Try again.")


def ask_owners(files_or_dirs: Tuple[Path]) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in files_or_dirs:
        picture_owners[picture] = ask_owner(file_or_dir=picture)
    return picture_owners
