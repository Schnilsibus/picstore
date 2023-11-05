from pathlib import Path
from typing import Optional
from datetime import datetime


class PicstoreException(Exception):
    def __init__(self, message: Optional[str] = None):
        Exception.__init__(self, message)


class MissingSubDirError(PicstoreException):
    def __init__(self, missing_dir: str):
        PicstoreException.__init__(self)
        self.missing_dir = missing_dir


class NotASubDirError(PicstoreException):
    def __init__(self, bad_directory: Path):
        PicstoreException.__init__(self)
        self.bad_directory = bad_directory


class PicDirNotFoundError(PicstoreException):
    def __init__(self, name: str, date: Optional[datetime.date]):
        PicstoreException.__init__(self)
        self.name = name
        self.date = date


class PicDirDuplicateError(PicstoreException):
    def __init__(self, name: str, date: Optional[datetime.date]):
        PicstoreException.__init__(self)
        self.name = name
        self.date = date
