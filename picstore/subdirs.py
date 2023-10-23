from collections.abc import Sequence
from pathlib import Path
from typing import Tuple


class SubDirectory(Sequence):
    def __init__(self, directory: Path):
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
