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


def pic_owner(picture: Path, use_metadata: bool, use_cli: bool) -> Ownership:
    owner = Ownership.Undefined
    if use_metadata:
        owner = evaluate_owner(picture=picture)
    if owner == Ownership.Undefined and use_cli:
        owner = ask_owner(item=picture)
    return owner


def pic_owners(pictures: Tuple[Path], use_metadata: bool, use_cli: bool) -> Dict[Path, Ownership]:
    owners = {}
    for picture in pictures:
        owners[picture] = pic_owner(picture=picture, use_metadata=use_metadata, use_cli=use_cli)
    return owners


def evaluate_owner(picture: Path) -> Ownership:
    model_tag = "EXIF:Model"
    with ExifToolHelper() as et:
        metadata = et.get_metadata(str(picture))[0]
        if model_tag in metadata:
            return Ownership.Own if metadata[model_tag] in _my_camera_models else Ownership.Other
        else:
            return Ownership.Undefined


def evaluate_owners(pictures: Tuple[Path]) -> Dict[Path, Ownership]:
    owners = {}
    for picture in pictures:
        owners[picture] = evaluate_owner(picture=picture)
    return owners


def ask_owner(item: Path | PicDir | ParentPicDir) -> Ownership:
    prefix = "please select ownership for item "
    suffix = " ['OWN' / 'OTHR']: "
    path = item
    if not type(item) == Path:
        path = item.path
    while True:
        owner = input(f"{prefix}{path}{suffix}").upper()
        if owner == "OWN":
            return Ownership.Own
        elif owner == "OTHR":
            return Ownership.Other
        else:
            print(f"\t -> {owner} is not a valid input. Try again.")
