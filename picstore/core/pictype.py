from exiftool import ExifToolHelper
import enum
from pathlib import Path
from typing import Tuple, Dict
from picstore.config import config


_raw_suffixes = config.raw_types
_std_suffixes = config.std_types
_my_camera_models = config.my_camera_models


class Category(enum.Enum):
    Std = enum.auto()
    Raw = enum.auto()
    Undefined = enum.auto()


class Ownership(enum.Enum):
    Own = enum.auto()
    Other = enum.auto()
    Undefined = enum.auto()


def category(path: Path) -> Category:
    if not path.is_file():
        return Category.Undefined
    suffix = path.suffix.upper()
    if suffix in _raw_suffixes:
        return Category.Raw
    elif suffix in _std_suffixes:
        return Category.Std
    else:
        return Category.Undefined


def categories(paths: Tuple[Path]) -> Dict[Path, Category]:
    picture_categories = {}
    for path in paths:
        picture_categories[path] = category(path=path)
    return picture_categories


def owner(path: Path, use_shell: bool = True) -> Ownership:
    picture_owner = evaluate_owner(path=path)
    if picture_owner == Ownership.Undefined and use_shell:
        picture_owner = ask_owner(path=path)
    return picture_owner


def owners(paths: Tuple[Path], use_shell: bool = True) -> Dict[Path, Ownership]:
    picture_owners = {}
    for path in paths:
        picture_owners[path] = owner(path=path, use_shell=use_shell)
    return picture_owners


def evaluate_owner(path: Path) -> Ownership:
    if not path.is_file():
        return Ownership.Undefined
    model_tag = "EXIF:Model"
    with ExifToolHelper() as et:
        metadata = et.get_metadata(str(path))[0]
        if model_tag in metadata:
            return Ownership.Own if metadata[model_tag] in _my_camera_models else Ownership.Other
        else:
            return Ownership.Undefined


def evaluate_owners(paths: Tuple[Path]) -> Dict[Path, Ownership]:
    picture_owners = {}
    for path in paths:
        picture_owners[path] = evaluate_owner(path=path)
    return picture_owners


def ask_owner(path: Path) -> Ownership:
    while True:
        picture_owner = input(f"please select ownership for {path} ('OWN' / 'OTHR'): ").upper()
        if picture_owner == "OWN":
            return Ownership.Own
        elif picture_owner == "OTHR":
            return Ownership.Other
        else:
            print(f"\t -> {picture_owner} is not a valid input. Try again.")


def ask_owners(paths: Tuple[Path]) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in paths:
        picture_owners[picture] = ask_owner(path=picture)
    return picture_owners


def get_type(path: Path, use_shell: bool = True) -> Tuple[Category, Ownership]:
    pic_category = category(path=path)
    pic_owner = owner(path=path, use_shell=use_shell)
    return pic_category, pic_owner


def get_types(paths: Tuple[Path], use_shell: bool = True) -> Dict[Path, Tuple[Category, Ownership]]:
    types = {}
    for path in paths:
        types[path] = get_type(path=path, use_shell=use_shell)
    return types
