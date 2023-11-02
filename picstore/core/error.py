from pathlib import Path
from typing import Optional
from datetime import datetime
from picstore.core.picdir import date_format


def raise_NotADirectoryError(path: Path) -> None:
    raise NotADirectoryError(f"{path} is no directory")


class SubDirError(ValueError):
    def __init__(self, path: Path):
        ValueError.__init__(self, f"{path} is not a SubDir")


class PicDirNotFoundError(KeyError):
    def __init__(self, name: str, date: Optional[datetime.date]):
        ValueError.__init__(self, PicDirNotFoundError._name_date_to_string(name=name, date=date))

    @staticmethod
    def _name_date_to_string(name: str, date: Optional[datetime.date]) -> str:
        date_addon = f"and date {date} "
        return f"No PicDir with name {name} {date_addon if date else ''}found"


class PicDirDuplicateError(ValueError):
    def __init__(self, name: str, date: Optional[datetime.date]):
        ValueError.__init__(self, PicDirDuplicateError._name_date_to_string(name=name, date=date))

    @staticmethod
    def _name_date_to_string(name: str, date: Optional[datetime.date]) -> str:
        date_addon = f"and date {date.strftime(date_format)} "
        return f"No PicDir with name {name} {date_addon if date else ''}found"
