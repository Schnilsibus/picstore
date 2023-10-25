from pathlib import Path
import datetime
from typing import Tuple, Optional, Dict
import shutil
from colorama import Fore, Style
from tqdm import tqdm
from picstore.config import config
from picstore.subdirs import RawDir, StdDir
import picstore.picowner as picowner
import picstore.piccategory as piccategory

date_format = "%Y-%m-%d"

_tab = "   "
_date_length = 10
_name_length = 20
_pic_count_length = 6
_pic_count_limit = 100000
_pic_count_exceeds_limit = ">=10^5"
_status_length = 6

_raw_suffixes = config.raw_types
_std_suffixes = config.std_types


class PicDir:
    required_directories = ["STD", "RAW", "EXP", "LR", "OTHR"]

    def __init__(
            self,
            path_or_parent: Path,
            name: Optional[str] = None,
            date: Optional[datetime.date] = None
    ):
        if (name is None and date is not None) or (name is not None and date is None):
            raise TypeError("name and date must either both have a value or both be None")
        if name is None:
            self._path = path_or_parent
            self._name, self._date = PicDir._path_to_name_and_date(path=self._path)
            self._directories = self._load_sub_directories()
        else:
            self._path = path_or_parent / f"{date.strftime(date_format)}_{name}"
            self._name = name
            self._date = date
            self._path.mkdir()
            self._directories = self._load_sub_directories(create=True)
        self._raw_dir = RawDir(directory=self._directories["RAW"])
        self._std_dir = StdDir(directory=self._directories["STD"])
        self.update()

    def __getitem__(self, item):
        return self._directories[item]

    def __eq__(self, other) -> bool:
        """

        :type other: PicDir
        """
        if not type(other) == PicDir:
            return False
        self.update()
        other.update()
        if not self._name == other._name:
            return False
        elif not self._date == other._date:
            return False
        return self.raw == other.raw and self.std == other.std

    def __str__(self):
        string = ""
        if len(self._name) > _name_length - 3:
            string += self._name[:-3] + "..." + _tab
        else:
            string += self._name.ljust(20) + _tab
        string += self._date.strftime(date_format) + _tab
        if self.raw_count > _pic_count_limit:
            string += ">=10^5" + _tab
        else:
            string += str(self.raw_count).ljust(_pic_count_length) + _tab
        if self.std_count > _pic_count_limit:
            string += ">=10^5" + _tab
        else:
            string += str(self.std_count).ljust(_pic_count_length) + _tab
        if self.is_intact():
            string += f"{Fore.GREEN}{'ok'.ljust(_status_length)}"
        else:
            string += f"{Fore.RED}{'bad'.ljust(_status_length)}"
        return f"{string}{Style.RESET_ALL}"

    @property
    def raw(self) -> RawDir:
        return self._raw_dir

    @property
    def std(self) -> StdDir:
        return self._std_dir

    def update(self) -> None:
        self.raw.update()
        self.std.update()

    def add(
            self,
            directory: Path,
            use_cli: bool = True,
            display_tqdm: bool = True
    ) -> int:
        files = tuple(directory.rglob("*.*"))
        owners = picowner.owners(files_or_dirs=files, use_cli=use_cli)
        categories = piccategory.categories(files=files)
        to_copy = {}
        for file in files:
            if self.raw.is_addable(picture=file, category=categories[file], owner=owners[file]):
                to_copy[file] = self.raw
            elif self.std.is_addable(picture=file, category=categories[file], owner=owners[file]):
                to_copy[file] = self.std
        iterator = tqdm(to_copy) if display_tqdm else to_copy
        for file in iterator:
            to_copy[file].add(picture=file, category=categories[file], owner=owners[file])
        return len(to_copy)

    def _load_sub_directories(self, create: bool = False) -> Dict[str, Path]:
        directories = {}
        for sub_dir in PicDir.required_directories:
            directories[sub_dir] = self._path / sub_dir
            if not directories[sub_dir].is_dir() and create:
                (self._path / sub_dir).mkdir()
            elif not directories[sub_dir].is_dir() and not create:
                raise IOError(f"The {sub_dir} sub directory is missing")
        return directories

    @staticmethod
    def _path_to_name_and_date(path: Path) -> Tuple[str, datetime.date]:
        start_date = datetime.datetime.strptime(path.name[:_date_length], date_format)
        name = path.name[_date_length + 1:]
        return name, start_date

    @staticmethod
    def table_header() -> str:
        string = "name".ljust(_name_length) + _tab
        string += "date".ljust(_date_length) + _tab
        string += "#raw".ljust(_pic_count_length) + _tab
        string += "#std".ljust(_pic_count_length) + _tab
        string += "status".ljust(_status_length)
        separator = "-" * len(string)
        return f"{Style.BRIGHT}{string}{Style.RESET_ALL}" + "\n" + separator

    @property
    def raw_count(self) -> int:
        return len(self.raw)

    @property
    def std_count(self) -> int:
        return len(self.std)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def date(self) -> datetime.date:
        return self._date

    def is_intact(self) -> bool:
        if not PicDir.is_name_correct(directory=self._path):
            return False
        if not PicDir.required_directories_exist(directory=self._path):
            return False
        if not len(self.raw.get_invalid_category_pictures()) == 0:
            return False
        if not len(self.std.get_invalid_category_pictures()) == 0:
            return False
        return True

    @staticmethod
    def is_name_correct(directory: Path) -> bool:
        if not directory.is_dir():
            raise ValueError(f"{str(directory)} is no directory")
        name = directory.parts[-1]
        try:
            assert name[4] == name[7] == "-"
            assert name[10] == "_"
            int(name[:4])
            int(name[5:7])
            int(name[8:10])
        except BaseException:
            return False
        return True

    @staticmethod
    def required_directories_exist(directory: Path) -> bool:
        if not directory.is_dir():
            raise ValueError(f"{str(directory)} is no directory")
        sub_directories = map(lambda d: d.parts[-1], directory.iterdir())
        return set(PicDir.required_directories) <= set(sub_directories)

    @staticmethod
    def rename_directory(directory: Path) -> Path:
        directory_name = directory.parts[-1]
        parts = directory_name.replace("-", "_").split("_")
        if len(parts) < 4:
            return directory
        try:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
        except ValueError:
            return directory
        if 0 <= year <= 99:
            year += 2000
        if year < 2000 or month < 0 or month > 12 or day < 0 or day > 31:
            return directory
        date = datetime.date(year=year, month=month, day=day)
        new_name = f"{date.strftime(date_format)}_{''.join(parts[3:])}"
        shutil.move(src=directory, dst=directory.parent / new_name)
        return Path(new_name)
