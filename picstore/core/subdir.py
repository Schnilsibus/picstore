from collections.abc import Sequence
from pathlib import Path
from typing import List, Generator, Set
import shutil
from picstore.core import pictype
from picstore.core.error import raise_no_directory, SubDirError


class SubDir(Sequence[Path]):

    possible_directory_names = ["RAW", "STD", "OTHR"]

    def __init__(self, directory: Path):
        Sequence.__init__(self)
        if not directory.is_dir():
            raise_no_directory(path=directory)
        if directory.name not in SubDir.possible_directory_names:
            raise SubDirError(path=directory)
        self._path = directory
        self._name = directory.name
        self._content = self._load_content()
        if directory.name == "RAW":
            self._categories = (pictype.Category.Raw, )
            self._owner = pictype.Ownership.Own
        elif directory.name == "STD":
            self._categories = (pictype.Category.Std, )
            self._owner = pictype.Ownership.Own
        elif directory.name == "OTHR":
            self._categories = (pictype.Category.Raw, pictype.Category.Raw)
            self._owner = pictype.Ownership.Other

    def __len__(self):
        return len(self._content)

    def __getitem__(self, item):
        return self._content[item]

    def _load_content(self) -> List[Path]:
        all_content = tuple(self.iterdir())
        return list(filter(lambda p: not self.is_ignored(path=p), all_content))

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    def iterdir(self) -> Generator[Path, None, None]:
        return self.path.iterdir()

    def is_addable(self, picture: Path) -> bool:
        return not (self.is_ignored(path=picture) and self.contains_name(name=picture.name))

    def is_ignored(self, path: Path) -> bool:
        if not path.is_file():
            return True
        if pictype.category(path=path) in self._categories:
            return False

    def contains_name(self, name: str) -> bool:
        return name in map(lambda p: p.name, self.iterdir())

    def add(self, picture: Path, copy: bool = True) -> bool:
        if not self.is_addable(picture=picture):
            return False
        shutil.copy2(src=picture, dst=self.path) if copy else shutil.move(src=picture, dst=self.path)
        return True

    def update(self) -> None:
        self._content = self._load_content()

    def get_invalid_category_content(self) -> Set[Path]:
        return set(filter(lambda p: pictype.category(path=p) not in self._categories, self.iterdir()))

    def get_invalid_owner_content(self) -> Set[Path]:
        return set(filter(lambda p: not pictype.owner(path=p) == self._owner, self.iterdir()))

    def is_intact(self) -> bool:
        if self.name == "OTHR":
            return True
        return len(self.get_invalid_category_content()) == 0
