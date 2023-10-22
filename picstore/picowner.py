import enum
from pathlib import Path
from exiftool import ExifToolHelper
from typing import Tuple, Dict
from picstore.picdir import PicDir
from picstore.parentpicdir import ParentPicDir
from picstore.config import config


_my_camera_models = config.my_camera_models


class Ownership(enum.Enum):
    Own = enum.auto()
    Other = enum.auto()
    Undefined = enum.auto()


def owner(picture: Path, use_metadata: bool, use_cli: bool) -> Ownership:
    picture_owner = Ownership.Undefined
    if use_metadata:
        picture_owner = evaluate_owner(picture=picture)
    if picture_owner == Ownership.Undefined and use_cli:
        picture_owner = ask_owner(item=picture)
    return picture_owner


def owners(pictures: Tuple[Path], use_metadata: bool, use_cli: bool) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in pictures:
        picture_owners[picture] = pic_owner(picture=picture, use_metadata=use_metadata, use_cli=use_cli)
    return picture_owners


def evaluate_owner(picture: Path) -> Ownership:
    model_tag = "EXIF:Model"
    with ExifToolHelper() as et:
        metadata = et.get_metadata(str(picture))[0]
        if model_tag in metadata:
            return Ownership.Own if metadata[model_tag] in _my_camera_models else Ownership.Other
        else:
            return Ownership.Undefined


def evaluate_owners(pictures: Tuple[Path]) -> Dict[Path, Ownership]:
    picture_owners = {}
    for picture in pictures:
        picture_owners[picture] = evaluate_owner(picture=picture)
    return picture_owners


def ask_owner(item: Path | PicDir | ParentPicDir) -> Ownership:
    prefix = "please select ownership for item "
    suffix = " ['OWN' / 'OTHR']: "
    path = item
    if not type(item) == Path:
        path = item.path
    while True:
        picture_owner = input(f"{prefix}{path}{suffix}").upper()
        if picture_owner == "OWN":
            return Ownership.Own
        elif picture_owner == "OTHR":
            return Ownership.Other
        else:
            print(f"\t -> {picture_owner} is not a valid input. Try again.")
