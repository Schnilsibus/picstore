from collections.abc import Sequence
from pathlib import Path
from typing import Tuple, Generator
import shutil
from picstore.core import pictype


class SubDir(Sequence[Path]):
    def __init__(self, directory: Path):
        Sequence.__init__(self)
        if not directory.is_dir():
            raise ValueError(f"{directory} is not a directory")
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

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def content(self) -> Tuple[Path]:
        return self._content

    def iterdir(self) -> Generator[Path, None, None]:
        return self.path.iterdir()

    def _load_content(self) -> Tuple[Path]:
        all_content = tuple(self.iterdir())
        types = pictype.get_types(all_content, use_shell=False)
        return tuple(filter(lambda key: not self.is_ignored(path=key, category=types[key][0]), types.keys()))

    def is_addable(self, picture: Path, category: pictype.Category) -> bool:
        if self.is_ignored(path=picture, category=category):
            return False
        if self.contains_name(name=picture.name):
            return False
        return True

    def is_ignored(self, path: Path, category: pictype.Category) -> bool:
        if not path.is_file():
            return True
        if category in self._categories:
            return False

    def contains_name(self, name: str) -> bool:
        return name in map(lambda p: p.name, self.iterdir())

    def add(
            self,
            picture: Path,
            copy: bool = True
    ) -> bool:
        pic_category = pictype.category(path=picture)
        if not self.is_addable(picture=picture, category=pic_category):
            return False
        shutil.copy2(src=picture, dst=self.path) if copy else shutil.move(src=picture, dst=self.path)
        return True

    def update(self) -> None:
        self._content = self._load_content()

    def get_invalid_category_content(self) -> Tuple[Path]:
        return tuple(filter(lambda p: pictype.category(path=p) not in self._categories, self.iterdir()))

    def get_invalid_owner_content(self) -> Tuple[Path]:
        return tuple(filter(lambda p: not pictype.owner(path=p) == self._owner, self.iterdir()))

    def is_intact(self) -> bool:
        return len(self.get_invalid_category_content()) == 0
