from collections.abc import Sequence
from pathlib import Path
from typing import List, Generator, Set
import shutil
from picstore.core import pictype
from picstore.core.error import NotASubDirError


class SubDir(Sequence[Path]):

    possible_directory_names = ["RAW", "STD", "OTHR"]

    def __init__(self, directory: Path):
        Sequence.__init__(self)
        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a directory")
        if directory.name not in SubDir.possible_directory_names:
            raise NotASubDirError(bad_directory=directory)
        self._path = directory
        self._name = directory.name
        if directory.name == "RAW":
            self._categories = (pictype.Category.Raw, )
            self._owners = (pictype.Ownership.Own, )
        elif directory.name == "STD":
            self._categories = (pictype.Category.Std, )
            self._owners = (pictype.Ownership.Own, )
        elif directory.name == "OTHR":
            self._categories = (pictype.Category.Raw, pictype.Category.Std)
            self._owners = (pictype.Ownership.Other, pictype.Ownership.Undefined)
        self._content = self._load_content()

    def __len__(self):
        return len(self._content)

    def __getitem__(self, item):
        return self._content[item]

    def _load_content(self) -> List[Path]:
        all_content = tuple(self.iterdir())
        types = pictype.get_types(paths=all_content, use_shell=False)
        return list(filter(lambda p: not self.is_ignored(path=p, category=types[p][0], owner=types[p][1]), all_content))

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    def iterdir(self) -> Generator[Path, None, None]:
        return self.path.iterdir()

    def is_addable(self, picture: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        is_ignored = self.is_ignored(path=picture, category=category, owner=owner)
        is_contained = self.contains_name(name=picture.name)
        return not is_ignored and not is_contained

    def is_ignored(self, path: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        if not path.is_file():
            return True
        if category not in self._categories:
            return True
        if owner not in self._owners:
            return True
        return False

    def contains_name(self, name: str) -> bool:
        return name in map(lambda p: p.name, self.iterdir())

    def add(self, picture: Path, category: pictype.Category, owner: pictype.Ownership, copy: bool = True) -> bool:
        if not self.is_addable(picture=picture, category=category, owner=owner):
            return False
        shutil.copy2(src=picture, dst=self.path) if copy else shutil.move(src=picture, dst=self.path)
        return True

    def update(self) -> None:
        self._content = self._load_content()

    def get_invalid_category_content(self) -> Set[Path]:
        pic_categories = pictype.categories(paths=tuple(self.iterdir()))
        return set(filter(lambda p: pic_categories[p] not in self._categories, pic_categories.keys()))

    def get_invalid_owner_content(self) -> Set[Path]:
        pic_owners = pictype.owners(paths=tuple(self.iterdir()), use_shell=False)
        return set(filter(lambda p: pic_owners[p] not in self._owners, pic_owners.keys()))

    def is_intact(self) -> bool:
        return len(self.get_invalid_category_content()) == 0
