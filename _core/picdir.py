from pathlib import Path
import datetime
from typing import Tuple, List, Union
from shutil import copy2
from tqdm import tqdm
from json_sett import Settings
from colorama import Fore, Style

# TODO: add documentation
# TODO: make it so that parent_or_path arg of PicDir constructor is of type Union[ParentPicDir, Path]

_tab = "   "
_date_format = "%Y-%m-%d"
_date_length = len(_date_format)
_name_length = 20
_pic_count_length = 6
_pic_count_limit = 100000
_pic_count_exceeds_limit = ">=10^5"
_status_length = 6


settings = Settings(Path(__file__).parent.parent / "data" / "config.json")
_raw_suffixes = settings.raw_types
_std_suffixes = settings.std_types


class ParentPicDir:
    def __init__(self, path: Path):
        self._path = path
        self._load_picdirs()

    @property
    def path(self) -> Path:
        return self._path

    def __iter__(self):
        return self._picdirs.__iter__()

    def __getitem__(self, item):
        return self._picdirs.__getitem__(item)

    def _load_picdirs(self) -> None:
        self._picdirs = []
        for path in self.path.iterdir():
            if not path.is_dir():
                raise IOError(f"{path} is not valid (only picdirs allowed)")
            else:
                self._picdirs.append(PicDir(path_or_parent=self.path))


class PicDir:
    _ALL_SUB_DIRECTORIES = ["STD", "RAW", "EXP", "LR", "OTHR"]

    def __init__(
            self,
            path_or_parent: Union[ParentPicDir, Path],
            name: str = None,
            date: datetime.date = None,
            source: Path = None
     ):
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
            self.add(source=source)

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
        string = self.date.strftime(_date_format) + _tab
        if len(self.name) > _name_length - 3:
            string += self.name[:-3] + "..." + _tab
        else:
            string += self.name.ljust(20) + _tab
        if self.num_raw_files > _pic_count_limit:
            string += ">=10^5/"
        else:
            string += str(self.num_raw_files).ljust(_pic_count_length)
        if self.num_std_files > _pic_count_limit:
            string += ">=10^5" + _tab
        else:
            string += str(self.num_std_files).ljust(_pic_count_length) + _tab
        if self.is_intact():
            string += f"{Fore.GREEN}{'ok'.ljust(_status_length)}"
        else:
            string += f"{Fore.RED}{'bad'.ljust(_status_length)}"
        return string

    def _load(self, path: Path) -> None:
        self.path = path
        self.name, self.date = PicDir._path_to_name_and_date(path=path)
        self._load_sub_directories()
        self._sync_with_file_system()

    def _create(self, parent_dir: ParentPicDir, name: str, date: datetime.date) -> None:
        self.path = parent_dir.path / f"{date.strftime(_date_format)}_{name}"
        self.name = name
        self.date = date
        self.path.mkdir()
        self._load_sub_directories(create=True)
        self._sync_with_file_system()

    def _sync_with_file_system(self) -> None:
        self._raw_files = list(self._directories["RAW"].iterdir())
        self._std_files = list(self._directories["STD"].iterdir())

    def _load_sub_directories(self, create: bool = False) -> None:
        for sub_dir in PicDir._ALL_SUB_DIRECTORIES:
            self._directories[sub_dir] = self.path / sub_dir
            if not self._directories[sub_dir].is_dir() and create:
                (self.path / sub_dir).mkdir()
            elif not self._directories[sub_dir].isdir() and not create:
                raise IOError(f"The {sub_dir} sub directory is missing")

    @staticmethod
    def _path_to_name_and_date(path: Path) -> Tuple[str, datetime.date]:
        start_date = datetime.datetime.strptime(path.name[:len(_date_format)], _date_format)
        name = path.name[len(_date_format) + 1:]
        return name, start_date

    @staticmethod
    def table_header() -> str:
        string = "date".ljust(_date_length) + _tab
        string += "name".ljust(_name_length) + _tab
        string += "#raw  /#std  ".ljust(_name_length) + _tab
        string += "status".ljust(_name_length)
        return f"{Style.BRIGHT}{string}"

    @property
    def num_raw_files(self) -> int:
        return len(self._raw_files)

    @property
    def num_std_files(self) -> int:
        return len(self._std_files)

    def add(self, source: Union[Path, List[Path]], display_tqdm: bool = True) -> int:
        if type(source) == list:
            return self.add_pictures(pictures=source, display_tqdm=display_tqdm)
        elif issubclass(type(source), Path):
            return self.add_directory(directory=source, display_tqdm=display_tqdm)
        else:
            raise TypeError("parameter 'source' must ba a 'pathlib.Path' or a list of 'pathlib.Path's")

    def add_directory(self, directory: Path, display_tqdm: bool = True) -> int:
        if not issubclass(type(directory), Path) or not directory.is_dir():
            raise TypeError("can only add existing directories")
        return self.add_pictures(pictures=list(directory.iterdir()), display_tqdm=display_tqdm)

    def add_pictures(self, pictures: List[Path], display_tqdm: bool = True) -> int:
        if not type(pictures) == list or not all([issubclass(type(picture), Path) for picture in pictures]):
            raise TypeError("parameter 'pictures' must must be a list of 'pathlib.Path's")
        to_copy = list(filter(lambda p: p.suffix.upper() in _raw_suffixes + _std_suffixes, pictures))
        current_file_names = list(map(lambda p: p.name, self._raw_files + self._std_files))
        to_copy = list(filter(lambda p: p not in current_file_names, to_copy))
        iterator = tqdm(to_copy) if display_tqdm else to_copy
        for picture in iterator:
            if picture.suffix.upper() in _raw_suffixes:
                copy2(picture, self._directories["RAW"])
            elif picture.suffix.upper() in _std_suffixes:
                copy2(picture, self._directories["STD"])
        self._sync_with_file_system()
        return len(to_copy)

    def is_intact(self) -> bool:
        if not PicDir.has_correct_name(directory=self.path):
            return False
        if not PicDir.contains_only_sub_directories(directory=self.path):
            return False
        invalid_raw_files, invalid_std_files = self.get_files_with_wrong_extension()
        return len(invalid_raw_files) + len(invalid_std_files) == 0

    def get_files_with_wrong_extension(self) -> Tuple[List, List]:
        self._sync_with_file_system()
        invalid_raw_files = [file for file in self._raw_files if file.suffix.upper() not in _raw_suffixes]
        invalid_std_files = [file for file in self._std_files if file.suffix.upper() not in _std_suffixes]
        return invalid_raw_files, invalid_std_files

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
        except AssertionError | ValueError:
            return False
        return True

    @staticmethod
    def contains_only_sub_directories(directory: Path) -> bool:
        if not directory.is_dir():
            raise ValueError(f"{str(directory)} is no directory")
        sub_directories = map(lambda d: d.parts[-1], directory.iterdir())
        return sorted(sub_directories) == sorted(PicDir._ALL_SUB_DIRECTORIES)
