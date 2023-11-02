from pathlib import Path
import datetime
from typing import Tuple, Optional, Dict
from colorama import Fore, Style
from tqdm import tqdm
from picstore.config import config
from picstore.core.subdir import SubDir
from picstore.core.error import raise_NotADirectoryError, SubDirError


date_format = "%Y-%m-%d"


_raw_suffixes = config.raw_types
_std_suffixes = config.std_types


class PicDir:
    required_directories = ["STD", "RAW", "EXP", "LR", "OTHR"]

    def __init__(self, path_or_parent: Path, name: Optional[str] = None, date: Optional[datetime.date] = None):
        if (name is None and date is not None) or (name is not None and date is None):
            raise TypeError("name and date must either both have a value or both be None")
        if not path_or_parent.is_dir():
            raise_NotADirectoryError(path=path_or_parent)
        if name is None:
            self._path = path_or_parent
            self._name, self._date = PicDir._parse_directory_name(directory=self._path)
        else:
            self._path = path_or_parent / f"{date.strftime(date_format)}_{name}"
            self._name = name
            self._date = date
            self._path.mkdir()
            PicDir.create_required_directories(self._path)
        self._directories = self._load_sub_directories()
        self._raw_directory = SubDir(directory=self._directories["RAW"])
        self._std_directory = SubDir(directory=self._directories["STD"])
        self._other_directory = SubDir(directory=self._directories["OTHR"])
        self.update()

    def __str__(self):
        self.update()
        tab = "   "
        string = ""
        if len(self.name) > 17:
            string += self.name[:-3] + "..." + tab
        else:
            string += self.name.ljust(20) + tab
        string += self.date.strftime(date_format) + tab
        if self.raw_count >= 10 ** 5:
            string += ">=10^5" + tab
        else:
            string += str(self.raw_count).ljust(6) + tab
        if self.std_count >= 10 ** 5:
            string += ">=10^5" + tab
        else:
            string += str(self.std_count).ljust(6) + tab
        if self.is_intact():
            string += f"{Fore.GREEN}{'ok'.ljust(6)}"
        else:
            string += f"{Fore.RED}{'bad'.ljust(6)}"
        return f"{string}{Style.RESET_ALL}"

    def _load_sub_directories(self) -> Dict[str, Path]:
        directories = {}
        for name in PicDir.required_directories:
            directories[name] = self.path / name
            if not directories[name].is_dir():
                raise SubDirError(path=directories[name])
        return directories

    @staticmethod
    def _parse_directory_name(directory: Path) -> Tuple[str, datetime.date]:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        date = datetime.datetime.strptime(directory.name[:10], date_format)
        name = directory.name[11:]
        return name, date

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def date(self) -> datetime.date:
        return self._date

    @property
    def raw(self) -> SubDir:
        return self._raw_directory

    @property
    def std(self) -> SubDir:
        return self._std_directory

    @property
    def other(self) -> SubDir:
        return self._other_directory

    @property
    def raw_count(self) -> int:
        return len(self.raw)

    @property
    def std_count(self) -> int:
        return len(self.std)

    def update(self) -> None:
        self.raw.update()
        self.std.update()
        self.other.update()

    def add(self, directory: Path, display_tqdm: bool = True, recursive: bool = True, copy: bool = False) -> int:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        content = tuple(directory.iterdir())
        if recursive:
            content = tuple(directory.rglob("*"))
        files_to_add = {}
        for file in content:
            if self.raw.is_addable(picture=file):
                files_to_add[file] = self.raw
            elif self.std.is_addable(picture=file):
                files_to_add[file] = self.std
        if len(files_to_add) == 0:
            return 0
        iterator = tqdm(files_to_add, desc=f"adding {directory.name}", unit="files") if display_tqdm else files_to_add
        for file in iterator:
            files_to_add[file].add(picture=file, copy=copy)
        return len(files_to_add)

    def is_intact(self) -> bool:
        if not PicDir.is_name_correct(directory=self._path):
            return False
        if not PicDir.required_directories_exist(directory=self._path):
            return False
        if not self.raw.is_intact() or not self.std.is_intact():
            return False
        return True

    @staticmethod
    def table_header() -> str:
        tab = "   "
        string = "name".ljust(20) + tab
        string += "date".ljust(10) + tab
        string += "#raw".ljust(6) + tab
        string += "#std".ljust(6) + tab
        string += "status".ljust(6)
        separator = "-" * len(string)
        return f"{Style.BRIGHT}{string}{Style.RESET_ALL}\n{separator}"

    @staticmethod
    def is_name_correct(directory: Path) -> bool:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        name = directory.name
        try:
            assert name[4] == name[7] == "-"
            assert name[10] == "_"
            int(name[:4])
            int(name[5:7])
            int(name[8:10])
        except AssertionError | ValueError:
            return False
        return True

    @staticmethod
    def required_directories_exist(directory: Path) -> bool:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        sub_directory_names = map(lambda d: d.name, directory.iterdir())
        return set(PicDir.required_directories) <= set(sub_directory_names)

    @staticmethod
    def create_required_directories(directory: Path) -> None:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        for sub_directory_name in PicDir.required_directories:
            subdir = directory / sub_directory_name
            if not subdir.is_dir():
                subdir.mkdir()

    @staticmethod
    def rename_directory(directory: Path) -> Path:
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        name = directory.name
        name_parts = name.replace("-", "_").split("_")
        if len(name_parts) < 4:
            return directory
        try:
            year = int(name_parts[0])
            month = int(name_parts[1])
            day = int(name_parts[2])
        except ValueError:
            return directory
        if 0 <= year <= 99:
            current_year = int(datetime.datetime.now().strftime("%Y"))
            current_century = current_year - current_year % 100
            year += current_century
        if year < 0 or month < 0 or month > 12 or day < 0 or day > 31:
            return directory
        date = datetime.date(year=year, month=month, day=day)
        new_name = f"{date.strftime(date_format)}_{''.join(name_parts[3:])}"
        return directory.rename(new_name)
