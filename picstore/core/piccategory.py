import enum
from pathlib import Path
from typing import Tuple, Dict
from app.config import config


_raw_suffixes = config.raw_types
_std_suffixes = config.std_types


class Category(enum.Enum):
    Std = enum.auto()
    Raw = enum.auto()
    Undefined = enum.auto()


def category(file: Path) -> Category:
    if not file.is_file():
        return Category.Undefined
    suffix = file.suffix.upper()
    if suffix in _raw_suffixes:
        return Category.Raw
    elif suffix in _std_suffixes:
        return Category.Std
    else:
        return Category.Undefined


def categories(files: Tuple[Path]) -> Dict[Path, Category]:
    types = {}
    for file in files:
        types[file] = category(file=file)
    return types
