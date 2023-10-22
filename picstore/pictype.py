import enum
from pathlib import Path
from typing import Tuple, Dict
from picstore.config import config


_raw_suffixes = config.raw_types
_std_suffixes = config.std_types


class PicType(enum.Enum):
    Std = enum.auto()
    Raw = enum.auto()
    Undefined = enum.auto()


def pic_type(file: Path) -> PicType:
    suffix = file.suffix.upper()
    if suffix in _raw_suffixes:
        return PicType.Raw
    elif suffix in _std_suffixes:
        return PicType.Std
    else:
        return PicType.Undefined


def pic_types(files: Tuple[Path]) -> Dict[Path, PicType]:
    types = {}
    for file in files:
        types[file] = pic_type(file=file)
    return types
