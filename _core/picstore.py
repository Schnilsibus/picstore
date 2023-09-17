from pathlib import Path
from fotodir import FotoDir
from datetime import date


def main():
    test_source = Path(r"C:\Users\Nils\Desktop\test_source")
    test_dir = FotoDir(path_or_parent=test_source.parent, name="Test", start_date=date.today(), source=test_source)
    print("done")


if __name__ == "__main__":
    main()
