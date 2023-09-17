import extend_json
from pathlib import Path
from typing import Union

# TODO: add documentation
# TODO: make it its own thing and add to git / pip
# TODO:     problems with extend_json:
# TODO:      - used any (builtin function) not Any (type from typing)
# TODO:        --> maybe not use Any but a Union with all possible json types
# TODO:        --> add a Property and a Object type: Object ^= dict; Property ^= Union[list, str, float, bool, None]
# TODO:      - name in the first docu-comment is jsonx not extend_json
# TODO:


_FILE = Path()
_FILE_AS_DICT = {}

use_dict = True

Setting = extend_json.Property


def select_file(path: Path) -> None:
    raise NotImplementedError()


def get_setting(name: str) -> Setting:
    if use_dict and name in _FILE_AS_DICT:
        return _FILE_AS_DICT[name]
    else:
        return extend_json.getProperty(filePath=_FILE, keys=(name, ))




def save_setting(name: str, value: Setting) -> None:
    raise NotImplementedError()


