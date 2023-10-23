from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Tuple, Union, Dict
import shutil
from tqdm import tqdm
import picstore.picowner as picowner
import picstore.piccategory as piccategory

# TODO: iterate recursivly?O
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
        return filename in map(lambda p: p._name, self)

    def add(
            self,
            pictures: Dict[Path, Tuple[piccategory.Category, picowner.Ownership]],
            display_tqdm: bool = True,
            copy: bool = True
    ) -> int:
        copy_or_move = shutil.copy2 if copy else shutil.move
        to_copy = []
        for picture in pictures:
            category, owner = pictures[picture]
            if self.contains_filename(filename=picture.name):
                continue
            if not self.check_picture(picture=picture, category=category, owner=owner):
                continue
            to_copy.append(picture)
        tqdm_desc = "copying files" if copy else "moving files"
        iterator = tqdm(to_copy, desc=tqdm_desc, unit="files") if display_tqdm else to_copy
        for picture in iterator:
            copy_or_move(picture, self.path)
        return len(to_copy)

    @abstractmethod
    def check_picture(self, picture: Path, category: piccategory.Category, owner: picowner.Ownership) -> bool:
        if category == piccategory.Category.Undefined or owner == picowner.Ownership.Undefined:
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

    def check_picture(self, picture: Path, category: piccategory.Category, owner: picowner.Ownership) -> bool:
        if not SubPicDir.check_picture(self=self, owner=owner, category=category):
            return False
        if not category == piccategory.Category.Raw:
            return False
        return True

    def get_invalid_category_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not piccategory.category(file=p) == piccategory.Category.Raw, self))

    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not picowner.owner(picture=p) == picowner.Ownership.Own, self))


class StdDir(SubPicDir):
    def __init__(self, directory: Path):
        SubPicDir.__init__(self, directory=directory)

    def check_picture(self, picture: Path, category: piccategory.Category, owner: picowner.Ownership) -> bool:
        if not SubPicDir.check_picture(self=self, owner=owner, category=category):
            return False
        if not category == piccategory.Category.Std:
            return False
        return True

    def get_invalid_category_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not piccategory.category(file=p) == piccategory.Category.Std, self))

    def get_invalid_owner_pictures(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not picowner.owner(picture=p) == picowner.Ownership.Own, self))
