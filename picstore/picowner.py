import enum
from picdir import PicDir, ParentPicDir
from pathlib import Path
from exiftool import ExifToolHelper
from json_sett import Settings
from typing import Tuple, Dict


settings = Settings(Path(__file__).parent.parent / "data" / "config.json")
my_camera_models = settings.my_camera_models


class Ownership(enum.Enum):
    Own = enum.auto()
    Other = enum.auto()
    Undefined = enum.auto()


def pic_ownership(pictures: Tuple[Path], use_metadata: bool, use_cli: bool) -> Dict[Path, Ownership]:
    owners = dict(zip(pictures, [Ownership.Undefined, ] * len(pictures)))
    if use_metadata:
        owners = evaluate_ownerships(pictures=pictures)
    if use_cli:
        for picture in pictures:
            if owners[picture] == Ownership.Undefined:
                owners[picture] = ask_ownership(item=picture)
    return owners


def evaluate_ownerships(pictures: Tuple[Path]) -> Dict[Path, Ownership]:
    model_tag = "EXIF:Model"
    owners = {}
    with ExifToolHelper() as et:
        metadata = et.get_metadata(list(pictures))
        for i, picture in enumerate(pictures):
            if model_tag in metadata[i]:
                owners[picture] = Ownership.Own if metadata[i][model_tag] in my_camera_models else Ownership.Other
            else:
                owners[picture] = Ownership.Undefined
    return owners


def ask_ownership(item: Path | PicDir | ParentPicDir) -> Ownership:
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
