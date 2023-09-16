from pathlib import Path
from datetime import Date

class FotoDir:
    def __init__(self, path: Path, name: str = None, date: Date = None):
        if (name is None and not date is None) or (not name is None and date is None):
            raise ArgumentError("name and date must either both have a value or both be None")
        if name is None:
            pass
        else:
            pass

    def load(self, path: Path) -> None:
        pass