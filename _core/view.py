from datetime import datetime
from typing import Tuple, List
from pathlib import Path
from picdir import PicDir, ParentPicDir
from cli import date_format
from argparse import Namespace
from colorama import Style, Fore


def view(directory: Path, name: str, date: datetime.date = None) -> Tuple[PicDir, List[Path], List[Path]]:
    parent_picdir = ParentPicDir(directory=directory)
    picdir = parent_picdir.get(name=name, date=date)
    if picdir is None:
        date_str = "" if date is None else f"with date {date.strftime(date_format)}"
        raise RuntimeError(f"picdir '{name}' {date_str} not found in {directory}")
    invalid_raw_files, invalid_std_files = picdir.get_files_with_wrong_extension()
    return picdir, invalid_raw_files, invalid_std_files


def cli_view(args: Namespace) -> None:
    try:
        picdir, invalid_raw_files, invalid_std_files = view(directory=args.dir,
                                                            name=args.name,
                                                            date=args.date)
    except RuntimeError as ex:
        print(ex)
        return
    print(f"{Style.BRIGHT}Information on PidDir '{picdir.name}':{Style.RESET_ALL}")
    print(f"Name: {picdir.name}")
    print(f"Date: {picdir.date}")
    print(f"Number of raw files: {picdir.num_raw_files}")
    print(f"Number of std files: {picdir.num_std_files}")
    print(f"Path: {picdir.path}")
    if picdir.is_intact():
        print(f"Status: {Fore.GREEN}ok{Style.RESET_ALL}")
    else:
        print(f"Status: {Fore.RED}bad{Style.RESET_ALL}")
    print("Invalid files in RAW:")
    print("\t" + "\n\t".join(map(lambda p: p.name, invalid_raw_files)))
    print("Invalid files in STD:")
    print("\t" + "\n\t".join(map(lambda p: p.name, invalid_raw_files)))
