from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Tuple
import shutil
import picstore.core.pictype as pictype


# TODO: make one class that determines which type of subdir it is by the directory param in __init__


class SubPicDir(ABC, Sequence[Path]):
    def __init__(self, directory: Path):
        ABC.__init__(self)
        Sequence.__init__(self)
        self._path = directory
        self._files = self._load_files()

    def __len__(self):
        return len(self._files)

    def __getitem__(self, item):
        return self._files[item]

    def _load_files(self) -> Tuple[Path]:
        return tuple(filter(lambda p: p.is_file(), self.path.iterdir()))

    @property
    def path(self):
        return self._path

    def contains_filename(self, filename: str) -> bool:
        return filename in map(lambda p: p.name, self)

    def add(
            self,
            picture: Path,
            category: pictype.Category,
            owner: pictype.Ownership,
            copy: bool = True
    ) -> bool:
        if not self.is_addable(picture=picture, category=category, owner=owner):
            return False
        shutil.copy2(picture, self.path) if copy else shutil.move(picture, self.path)

    def update(self):
        self._files = self._load_files()

    @abstractmethod
    def is_addable(self, picture: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        if not picture.is_file():
            return False
        if self.contains_filename(filename=picture.name):
            return False
        if category == pictype.Category.Undefined or owner == pictype.Ownership.Undefined:
            return False
        return True

    @abstractmethod
    def get_invalid_category_pictures(self) -> Tuple[Path]:
        raise NotImplementedError()

    @abstractmethod
    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        raise NotImplementedError()


class RawDir(SubPicDir):
    def __init__(self, directory: Path):
        SubPicDir.__init__(self, directory=directory)

    def is_addable(self, picture: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        if not SubPicDir.is_addable(self=self, picture=picture, owner=owner, category=category):
            return False
        if not category == pictype.Category.Raw:
            return False
        return True

    def get_invalid_category_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.category(file=p) == pictype.Category.Raw, self))

    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.owner(file_or_dir=p, use_shell=False) == pictype.Ownership.Own,
                            self))


class StdDir(SubPicDir):
    def __init__(self, directory: Path):
        SubPicDir.__init__(self, directory=directory)

    def is_addable(self, picture: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        if not SubPicDir.is_addable(self=self, picture=picture, owner=owner, category=category):
            return False
        if not category == pictype.Category.Std:
            return False
        return True

    def get_invalid_category_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.category(file=p) == pictype.Category.Std, self))

    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.owner(file_or_dir=p, use_shell=False) == pictype.Ownership.Own,
                            self))


class OtherDir(SubPicDir):
    def __init__(self, directory: Path):
        SubPicDir.__init__(self, directory=directory)

    def is_addable(self, picture: Path, category: pictype.Category, owner: pictype.Ownership) -> bool:
        return SubPicDir.is_addable(self=self, picture=picture, category=category, owner=owner)

    def get_invalid_category_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: pictype.category(file=p) == pictype.Category.Undefined, self))

    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.owner(file_or_dir=p, use_shell=False) == pictype.Ownership.Other,
                            self))
