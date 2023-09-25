from pathlib import Path
from typing import List


# TODO: add documentation
# TODO: maybe use the pattern I found on the internet (Adapter pattern: https://stackoverflow.com/questions/7139111/python-extension-methods)
# TODO: make it its own project; upload to pip

def recursive_iterdir(path: Path) -> List[Path]:
    contents = list(path.iterdir())
    for file_or_dir in contents:
        if file_or_dir.is_dir():
            contents += recursive_iterdir(path=file_or_dir)
    return contents


def iterdir_only_files(path: Path) -> List[Path]:
    contents = list(path.iterdir())
    return [file for file in contents if file.is_file()]


def iterdir_only_dirs(path: Path) -> List[Path]:
    contents = list(path.iterdir())
    return [file for file in contents if file.is_dir()]


def recursive_iterdir_only_files(path: Path) -> List[Path]:
    dirs = list(iterdir_only_dirs(path=path))
    files = list(iterdir_only_files(path=path))
    for sub_dir in dirs:
        files += recursive_iterdir_only_files(path=sub_dir)
    return files


def recursive_iterdir_only_dirs(path: Path) -> List[Path]:
    dirs = list(iterdir_only_dirs(path=path))
    for sub_dir in dirs:
        dirs += recursive_iterdir_only_dirs(path=sub_dir)
    return dirs
