import enum
from picdir import PicDir, ParentPicDir
from pathlib import Path


class Ownership(enum.Enum):
    Own = enum.auto()
    Other = enum.auto()
    Undefined = enum.auto()


def pic_ownership(picture: Path, use_metadata: bool) -> Ownership:
    if not use_metadata:
        return ask_ownership(item=picture)
    else:
        return evaluate_ownership(picture=picture)


def evaluate_ownership(picture: Path) -> Ownership:
    raise NotImplementedError()


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