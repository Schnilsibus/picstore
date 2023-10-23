from pathlib import Path
from typing import Iterator, Union, List
from datetime import datetime
from picstore.picdir import PicDir, date_format


# TODO: implement proper indexable object: len; reverse etc. --> use appropriate SuperClass "Sequence"?


class ParentPicDir:
    def __init__(self, directory: Path):
        self._path = directory
        self._load_picdirs()

    @property
    def path(self) -> Path:
        return self._path

    def __iter__(self) -> Iterator[PicDir]:
        return self._picdirs.__iter__()

    def __getitem__(self, item) -> PicDir:
        return self._picdirs[item]

    def get(self, name: str, date: datetime.date = None) -> PicDir | None:
        for picdir in self:
            if date is None and picdir._name == name:
                return picdir
            elif date is not None and picdir._name == name and picdir._date == date:
                return picdir
        return None

    def add(self, name: str, date: datetime.date, source: Union[Path, List[Path]]) -> PicDir:
        if self.get(name=name, date=date) is not None:
            raise RuntimeError(f"picdir '{name}' with date {date.strftime(date_format)} already exists in {self.path}")
        new_picdir = PicDir(path_or_parent=self.path, name=name, date=date, source=source)
        self._picdirs.append(new_picdir)
        return new_picdir

    def _load_picdirs(self) -> None:
        self._picdirs = []
        for path in self.path.iterdir():
            try:
                self._picdirs.append(PicDir(path_or_parent=path))
            except Exception:
                pass
