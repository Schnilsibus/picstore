import enum
from pathlib import Path
from json_sett import Settings

settings = Settings(Path(__file__).parent.parent / "data" / "config.json")
raw_suffixes = settings.raw_types
std_suffixes = settings.std_types


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
