from pathlib import Path
from typing import List, Optional, Literal
from datetime import datetime
from collections.abc import Sequence
from picstore.core.picdir import PicDir, date_format


class ParentDir(Sequence[PicDir]):
    def __init__(self, directory: Path):
        Sequence.__init__(self)
        self._path = directory
        self._picdirs = self._load_picdirs()

    @property
    def path(self) -> Path:
        return self._path

    def __len__(self):
        return len(self._picdirs)

    def __getitem__(self, item):
        return self._picdirs[item]

    def _load_picdirs(self) -> List[PicDir]:
        picdirs = []
        for path in self.path.iterdir():
            try:
                picdirs.append(PicDir(path_or_parent=path))
            except Exception:
                pass
        return picdirs

    def get(self, name: str, date: Optional[datetime.date] = None) -> PicDir:
        for picdir in self:
            if date is None and picdir.name == name:
                return picdir
            elif date is not None and picdir.name == name and picdir.date == date:
                return picdir
        message = f"No picdir with name {name}"
        if date is not None:
            message += f" and date {date.strftime(date_format)}"
        raise KeyError(message)

    def exists(self, name: str, date: Optional[datetime.date] = None) -> bool:
        try:
            self.get(name=name, date=date)
            return True
        except KeyError:
            return False

    def add(self, name: str, date: datetime.date) -> PicDir:
        if self.exists(name=name, date=date):
            raise RuntimeError(f"picdir '{name}' with date {date.strftime(date_format)} already exists in {self.path}")
        new_picdir = PicDir(path_or_parent=self.path, name=name, date=date)
        self._picdirs.append(new_picdir)
        return new_picdir

    def sort(self, attribute: Literal["name", "date", "raw", "std"] = "date") -> None:
        if attribute == "name":
            self._picdirs.sort(key=lambda p: p.name)
        if attribute == "date":
            self._picdirs.sort(key=lambda p: p.date)
        if attribute == "raw":
            self._picdirs.sort(key=lambda p: p.count_raw)
        if attribute == "date":
            self._picdirs.sort(key=lambda p: p.count_std)
