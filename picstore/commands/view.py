from datetime import datetime
from typing import Tuple, Optional
from pathlib import Path
from colorama import Style, Fore
from core.parentpicdir import ParentPicDir
from app.cli import date_format


def view(directory: Path, name: str, date: Optional[datetime.date] = None) -> None:
    parent_picdir = ParentPicDir(directory=directory)
    picdir = parent_picdir.get(name=name, date=date)
    if picdir is None:
        date_str = "" if date is None else f"with date {date.strftime(date_format)}"
        raise RuntimeError(f"picdir '{name}' {date_str} not found in {directory}")
    title = f"Information on PicDir '{picdir._name}':"
    print(f"{Style.BRIGHT}{title}{Style.RESET_ALL}" + "\n" + "-" * len(title))
    print(f"{'Name:'.ljust(10)}{picdir._name}")
    print(f"{'Date:'.ljust(10)}{picdir._date.strftime(date_format)}")
    print(f"{'#RAW:'.ljust(10)}{picdir.num_raw_files}")
    print(f"{'#STD:'.ljust(10)}{picdir.num_std_files}")
    print(f"{'Path:'.ljust(10)}{picdir._path}")
    if picdir.is_intact():
        print(f"{'Status:'.ljust(10)}{Fore.GREEN}ok{Style.RESET_ALL}")
    else:
        print(f"{'Status:'.ljust(10)}{Fore.RED}bad{Style.RESET_ALL}")
    print()
    print_files(title=f"Invalid in {picdir._path}", files=picdir.wrong_category_files(directory="TOP"))
    print_files(title=f"Invalid in {picdir._path / 'RAW'}", files=picdir.wrong_category_files(directory="RAW"))
    print_files(title=f"Invalid in {picdir._path / 'RAW'}", files=picdir.wrong_category_files(directory="STD"))


def print_files(title: str, files: Tuple[Path]) -> None:
    print(title)
    if len(files) > 0:
        print("\t" + "\n\t".join(map(lambda p: p._name, files)))
    else:
        print("\t---")
