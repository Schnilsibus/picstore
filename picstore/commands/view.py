from datetime import datetime
from typing import Tuple, List
from pathlib import Path
from argparse import Namespace
from colorama import Style, Fore
from picstore.picdir import PicDir
from picstore.parentpicdir import ParentPicDir
from picstore.cli import date_format


def view(directory: Path, name: str, date: datetime.date = None) -> Tuple[PicDir, List[Path], List[Path]]:
    parent_picdir = ParentPicDir(directory=directory)
    picdir = parent_picdir.get(name=name, date=date)
    if picdir is None:
        date_str = "" if date is None else f"with date {date.strftime(date_format)}"
        raise RuntimeError(f"picdir '{name}' {date_str} not found in {directory}")
    invalid_raw_files, invalid_std_files = picdir.wrong_files()
    return picdir, invalid_raw_files, invalid_std_files


def cli_view(args: Namespace) -> None:
    try:
        picdir, invalid_raw_files, invalid_std_files = view(directory=args.dir,
                                                            name=args.name,
                                                            date=args.date)
    except RuntimeError as ex:
        print(ex)
        return
    title = f"Information on PicDir '{picdir.name}':"
    print(f"{Style.BRIGHT}{title}{Style.RESET_ALL}" + "\n" + "-" * len(title))
    print(f"{'Name:'.ljust(10)}{picdir.name}")
    print(f"{'Date:'.ljust(10)}{picdir.date.strftime(date_format)}")
    print(f"{'#RAW:'.ljust(10)}{picdir.num_raw_files}")
    print(f"{'#STD:'.ljust(10)}{picdir.num_std_files}")
    print(f"{'Path:'.ljust(10)}{picdir.path}")
    if picdir.is_intact():
        print(f"{'Status:'.ljust(10)}{Fore.GREEN}ok{Style.RESET_ALL}")
    else:
        print(f"{'Status:'.ljust(10)}{Fore.RED}bad{Style.RESET_ALL}")
    print()
    print("Invalid files in RAW:")
    if len(invalid_raw_files) > 0:
        print("\t" + "\n\t".join(map(lambda p: p.name, invalid_raw_files)))
    else:
        print("\t---")
    print("Invalid files in STD:")
    if len(invalid_std_files) > 0:
        print("\t" + "\n\t".join(map(lambda p: p.name, invalid_std_files)))
    else:
        print("\t---")
