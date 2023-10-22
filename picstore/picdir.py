from pathlib import Path
import datetime
from typing import Tuple, List, Union, Literal, Optional, Dict
import shutil
from tqdm import tqdm
from colorama import Fore, Style
from picstore.piccategory import Category, categories
from picstore.picowner import Ownership, owners
from picstore.config import config

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
    _all_sub_directories = ["STD", "RAW", "EXP", "LR", "OTHR"]

    def __init__(
            self,
            path_or_parent: Path,
            name: Optional[str] = None,
            date: Optional[datetime.date] = None,
            source: Optional[Union[Path, List[Path]]] = None,
            display_tqdm: bool = True,
            create_dirs: bool = False
     ):
        if (name is None and date is not None) or (name is not None and date is None):
            raise TypeError("name and date must either both have a value or both be None")
        self._directories: Dict[str, Path] = {}
        self._raw_files: List[Path] = []
        self._std_files: List[Path] = []
        if name is None:
            self._load(path=path_or_parent, create_dirs=create_dirs)
        else:
            self._create(parent_dir=path_or_parent, name=name, date=date)
        if source:
            self.add(source=source, display_tqdm=display_tqdm)

    def __eq__(self, other) -> bool:
        """

        :type other: PicDir
        """
        if not type(other) == PicDir:
            return False
        self._sync_with_file_system()
        other._sync_with_file_system()
        if not self.name == other.name:
            return False
        elif not self.date == other.date:
            return False
        elif not self._raw_files == other._raw_files:
            return False
        elif not self._std_files == other._raw_files:
            return False
        else:
            return True

    def __str__(self):
        string = ""
        if len(self.name) > _name_length - 3:
            string += self.name[:-3] + "..." + _tab
        else:
            string += self.name.ljust(20) + _tab
        string += self.date.strftime(date_format) + _tab
        if self.num_raw_files > _pic_count_limit:
            string += ">=10^5" + _tab
        else:
            string += str(self.num_raw_files).ljust(_pic_count_length) + _tab
        if self.num_std_files > _pic_count_limit:
            string += ">=10^5" + _tab
        else:
            string += str(self.num_std_files).ljust(_pic_count_length) + _tab
        if self.is_intact():
            string += f"{Fore.GREEN}{'ok'.ljust(_status_length)}"
        else:
            string += f"{Fore.RED}{'bad'.ljust(_status_length)}"
        return f"{string}{Style.RESET_ALL}"

    def _load(self, path: Path, create_dirs: bool) -> None:
        self.path = path
        self.name, self.date = PicDir._path_to_name_and_date(path=path)
        self._load_sub_directories(create=create_dirs)
        self._sync_with_file_system()

    def _create(self, parent_dir: Path, name: str, date: datetime.date) -> None:
        self.path = parent_dir / f"{date.strftime(date_format)}_{name}"
        self.name = name
        self.date = date
        self.path.mkdir()
        self._load_sub_directories(create=True)
        self._sync_with_file_system()

    def _sync_with_file_system(self) -> None:
        self._raw_files = list(self._directories["RAW"].iterdir())
        self._std_files = list(self._directories["STD"].iterdir())

    def _load_sub_directories(self, create: bool = False) -> None:
        for sub_dir in PicDir._all_sub_directories:
            self._directories[sub_dir] = self.path / sub_dir
            if not self._directories[sub_dir].is_dir() and create:
                (self.path / sub_dir).mkdir()
            elif not self._directories[sub_dir].is_dir() and not create:
                raise IOError(f"The {sub_dir} sub directory is missing")

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
    def num_raw_files(self) -> int:
        return len(self._raw_files)

    @property
    def num_std_files(self) -> int:
        return len(self._std_files)

    def add(self, source: Union[Path, Tuple[Path]], display_tqdm: bool = True, recursive: bool = True) -> int:
        if type(source) == tuple:
            return self.add_pictures(pictures=source, display_tqdm=display_tqdm)
        elif issubclass(type(source), Path):
            return self.add_directory(directory=source, display_tqdm=display_tqdm, recursive=recursive)
        else:
            raise TypeError("parameter 'source' must ba a 'pathlib.Path' or a list of 'pathlib.Path's")

    def add_directory(self, directory: Path, display_tqdm: bool = True, recursive: bool = True) -> int:
        if not issubclass(type(directory), Path) or not directory.is_dir():
            raise TypeError("can only add existing directories")
        if not recursive:
            return self.add_pictures(pictures=tuple(directory.iterdir()), display_tqdm=display_tqdm)
        else:
            return self.add_pictures(pictures=tuple(directory.rglob("*.*")), display_tqdm=display_tqdm)

    def add_pictures(
            self,
            pictures: Tuple[Path],
            display_tqdm: bool = True,
            picture_owner: Optional[Ownership] = None,
            use_metadata: bool = True,
            use_cli: bool = True,
            copy: bool = False
    ) -> int:
        # TODO: construct a {source. dest} dict with only files that can be moved an only then move them and display tqdm --> two for loops
        if not type(pictures) == tuple or not all([issubclass(type(picture), Path) for picture in pictures]):
            raise TypeError("parameter 'pictures' must must be a list of 'pathlib.Path's")
        count = 0
        copy_or_move = shutil.copy2 if copy else shutil.move
        types = categories(files=pictures)
        picture_owners = None
        if picture_owner is None:
            picture_owners = owners(pictures=pictures, use_cli=use_cli, use_metadata=use_metadata)
        tqdm_desc = "copying files" if copy else "moving files"
        iterator = tqdm(pictures, desc=tqdm_desc, unit="files") if display_tqdm else pictures
        for picture in iterator:
            picture_owner = picture_owner if picture_owner is not None else picture_owners[picture]
            picture_type = types[picture]
            dest = picture.parent
            if picture_type == Category.Undefined or picture_owner == Ownership.Undefined:
                continue
            elif picture_owner == Ownership.Other:
                dest = self._directories["OTHR"]
            elif picture_owner == Ownership.Own and picture_type == Category.Raw:
                dest = self._directories["RAW"]
            elif picture_owner == Ownership.Own and picture_type == Category.Std:
                dest = self._directories["STD"]
            if picture.name not in map(lambda p: p.name, dest.iterdir()):
                copy_or_move(picture, dest)
            count += 1
        return count

    def is_intact(self) -> bool:
        if not PicDir.has_correct_name(directory=self.path):
            return False
        if not PicDir.contains_sub_directories(directory=self.path):
            return False
        if not len(self.wrong_category_files(directory="RAW")) == 0:
            return False
        if not len(self.wrong_category_files(directory="STD")) == 0:
            return False
        if not len(self.wrong_category_files(directory="TOP")) == 0:
            return False
        return True

    def wrong_category_files(self, directory: Literal["RAW", "STD", "TOP"]) -> Tuple[Path]:
        self._sync_with_file_system()
        all_files = tuple(self._raw_files if directory == "RAW" else self._std_files)
        if directory == "TOP":
            all_files = tuple(self.path.iterdir())
        all_categories = categories(files=all_files)
        if directory == "RAW":
            return tuple(filter(lambda file: not all_categories[file] == Category.Raw, all_files))
        elif directory == "STD":
            return tuple(filter(lambda file: not all_categories[file] == Category.Std, all_files))
        elif directory == "TOP":
            return tuple(filter(lambda file: not all_categories[file] == Category.Undefined, all_files))

    def wrong_ownership_files(self, directory: Literal["RAW", "STD", "OTHR"]) -> Tuple[Tuple[Path], Tuple[Path]]:
        self._sync_with_file_system()
        all_files = tuple(self._raw_files if directory == "RAW" else self._std_files)
        if directory == "OTHR":
            all_files = tuple(self._directories["OTHR"].iterdir())
        all_owners = owners(pictures=all_files, use_cli=False, use_metadata=True)
        undefined_files = tuple(filter(lambda file: all_owners[file] == Ownership.Undefined, all_files))
        if directory == "RAW" or directory == "STD":
            return tuple(filter(lambda file: all_owners[file] == Ownership.Other, all_files)), undefined_files
        elif directory == "OTHR":
            return tuple(filter(lambda file: all_owners[file] == Ownership.Own, all_files)), undefined_files

    @staticmethod
    def has_correct_name(directory: Path) -> bool:
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
    def contains_sub_directories(directory: Path) -> bool:
        if not directory.is_dir():
            raise ValueError(f"{str(directory)} is no directory")
        sub_directories = map(lambda d: d.parts[-1], directory.iterdir())
        return set(PicDir._all_sub_directories) <= set(sub_directories)

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
