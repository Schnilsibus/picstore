from pathlib import Path
from typing import List, Optional, Literal
from datetime import datetime
from collections.abc import Sequence
from picstore.core.picdir import PicDir
from picstore.core.error import raise_NotADirectoryError, PicDirNotFoundError, PicDirDuplicateError


class ParentDir(Sequence[PicDir]):
    def __init__(self, directory: Path):
        Sequence.__init__(self)
        if not directory.is_dir():
            raise_NotADirectoryError(path=directory)
        self._path = directory
        self._picdirs = self._load_picdirs()

    def __len__(self):
        return len(self._picdirs)

    def __getitem__(self, item):
        return self._picdirs[item]

    def _load_picdirs(self) -> List[PicDir]:
        picdirs = []
        for path in self.path.iterdir():
            if not path.is_dir():
                continue
            elif not PicDir.is_name_correct(directory=path):
                continue
            elif PicDir.required_directories_exist(directory=path):
                continue
            picdirs.append(PicDir(path_or_parent=path))
        return picdirs

    @property
    def path(self) -> Path:
        return self._path

    def get(self, name: str, date: Optional[datetime.date] = None) -> PicDir:
        for picdir in self:
            if date is None and picdir.name == name:
                return picdir
            elif date is not None and picdir.name == name and picdir.date == date:
                return picdir
        raise PicDirNotFoundError(name=name, date=date)

    def exists(self, name: str, date: Optional[datetime.date] = None) -> bool:
        try:
            self.get(name=name, date=date)
            return True
        except PicDirNotFoundError:
            return False

    def add(self, name: str, date: datetime.date) -> PicDir:
        if self.exists(name=name, date=date):
            raise PicDirDuplicateError(name=name, date=date)
        new_picdir = PicDir(path_or_parent=self.path, name=name, date=date)
        self._picdirs.append(new_picdir)
        return new_picdir

    def sort(self, attribute: Literal["name", "date", "raw", "std"] = "date") -> None:
        if attribute == "name":
            self._picdirs.sort(key=lambda p: p.name)
        elif attribute == "date":
            self._picdirs.sort(key=lambda p: p.date)
        elif attribute == "raw":
            self._picdirs.sort(key=lambda p: p.count_raw)
        elif attribute == "std":
            self._picdirs.sort(key=lambda p: p.count_std)

    def update(self) -> None:
        self._picdirs = self._load_picdirs()
