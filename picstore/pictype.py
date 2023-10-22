import enum
from pathlib import Path
from picstore.config import config


raw_suffixes = config.raw_types
std_suffixes = config.std_types


class PicType(enum.Enum):
    Std = enum.auto()
    Raw = enum.auto()
    Undefined = enum.auto()


def pic_type(file: Path) -> PicType:
    suffix = file.suffix.upper()
    if suffix in raw_suffixes:
        return PicType.Raw
    elif suffix in std_suffixes:
        return PicType.Std
    else:
        return PicType.Undefined
