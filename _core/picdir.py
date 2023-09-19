from pathlib import Path
import datetime
from typing import Tuple, List
from shutil import copy2

# TODO: add documentation
# TODO: maybe add settings file --> a setting would me the file extensions that are accepted as RAW / STD file
# TODO: dont use __add__ but std public method add
# TODO: in add ignore files that are already present in the target dir
# TODO:  --> return the number of added files (NOT files found in source)
# TODO: change to PicDir and picdir.py


_tab = "  "
_chars_name = 20
_name_not_displayed_completely = "..."
_chars_pic_count = 6
_pic_count_limit = 100000
_pic_count_exceeds_limit = ">=10^5"


class NotAPicDirError(Exception):
    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class PicDir:

    _DATE_FORMAT = "%Y-%m-%d"
    _ALL_SUB_DIRS = ["STD", "RAW", "EXP", "LR", "OTHR"]
    _RAW_SUFFIXES = [".CR2", ".DNG"]
    _STD_SUFFIXES = [".STD", ".JPG", ".JPEG", ".DNG"]

    def __init__(self, path_or_parent: Path, name: str = None, date: datetime.date = None, source: Path = None):
        if (name is None and date is not None) or (name is not None and date is None):
            raise TypeError("name and date must either both have a value or both be None")
        self._directories = {}
        self._raw_files = []
        self._std_files = []
        if name is None:
            self._load(path=path_or_parent)
        else:
            self._create(parent_dir=path_or_parent, name=name, date=date)
        if source:
            self.add_pictures(path=source)

    def add_pictures(self, path: Path) -> int:
        if not issubclass(type(path), Path) or not path.is_dir():
            raise TypeError("can only add existing directories")
        files = list(path.iterdir())
        raw_files = [file for file in files if file.suffix.upper() in PicDir._RAW_SUFFIXES]
        std_files = [file for file in files if file.suffix.upper() in PicDir._STD_SUFFIXES]
        for file in raw_files:
            copy2(file, self._directories["RAW"])
        for file in std_files:
            copy2(file, self._directories["STD"])
        self._sync_with_file_system()
        return len(raw_files) + len(std_files)

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def __str__(self):
        string = self.date.strftime(PicDir._DATE_FORMAT) + _tab
        if len(self.name) > _chars_name - 3:
            string += self.name[:-3] + _name_not_displayed_completely + _tab
        else:
            string += self.name.ljust(20) + _tab
        if self.num_raw_files > _pic_count_limit:
            string += _pic_count_exceeds_limit + "/"
        else:
            string += str(self.num_raw_files).ljust(_chars_pic_count)
        if self.num_std_files > _pic_count_limit:
            string += _pic_count_exceeds_limit
        else:
            string += str(self.num_std_files).ljust(_chars_pic_count)
        return string

    def _load(self, path: Path) -> None:
        self.path = path
        self.name, self.date = PicDir._path_to_name_date(path=path)
        self._fill_sub_dirs_dict()
        self._sync_with_file_system()

    def _create(self, parent_dir: Path, name: str, date: datetime.date) -> None:
        self.path = parent_dir / f"{date.strftime(PicDir._DATE_FORMAT)}_{name}"
        self.name = name
        self.date = date
        self.path.mkdir()
        self._fill_sub_dirs_dict(create=True)
        self._sync_with_file_system()

    def _sync_with_file_system(self) -> None:
        self._raw_files = self._directories["RAW"].iterdir()
        self._std_files = self._directories["STD"].iterdir()

    def _fill_sub_dirs_dict(self, create: bool = False) -> None:
        for sub_dir in PicDir._ALL_SUB_DIRS:
            self._directories[sub_dir] = self.path / sub_dir
            if not self._directories[sub_dir].is_dir() and create:
                (self.path / sub_dir).mkdir()
            elif not self._directories[sub_dir].isdir() and not create:
                raise NotAPicDirError(f"The {sub_dir} sub directory is missing")

    @staticmethod
    def _path_to_name_date(path: Path) -> Tuple[str, datetime.date]:
        start_date = datetime.datetime.strptime(path.name[:len(PicDir._DATE_FORMAT)], PicDir._DATE_FORMAT)
        name = path.name[len(PicDir._DATE_FORMAT) + 1:]
        return name, start_date

    @property
    def num_raw_files(self) -> int:
        return len(self._raw_files)

    @property
    def num_std_files(self) -> int:
        return len(self._std_files)

    def is_intact(self) -> bool:
        invalid_raw_files, invalid_std_files = self.integrity_report()
        return len(invalid_raw_files) + len(invalid_std_files) == 0

    def integrity_report(self) -> Tuple[List, List]:
        self._sync_with_file_system()
        invalid_raw_files = [file for file in self._raw_files if file.suffix.upper() not in PicDir._RAW_SUFFIXES]
        invalid_std_files = [file for file in self._std_files if file.suffix.upper() not in PicDir._STD_SUFFIXES]
        return invalid_raw_files, invalid_std_files
