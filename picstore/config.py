from json_sett import Settings
from pathlib import Path

_config_file = Path(__file__).parent / "data" / "config.json"

config = Settings(file=_config_file)
