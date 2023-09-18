import extend_json
from pathlib import Path

# TODO: add documentation
# TODO: make it its own thing and add to git / pip
# TODO:     problems with extend_json:
# TODO:      - used any (builtin function) not Any (type from typing)
# TODO:        --> maybe not use Any but a Union with all possible json types
# TODO:        --> add a Property and a Object type: Object ^= dict; Property ^= Union[list, str, float, bool, None]
# TODO:      - name in the first docu-comment is jsonx not extend_json


Setting = extend_json.Property


class Settings:
    def __init__(self, path: Path):
        self._FILE = path

    def __getattr__(self, name: str) -> Setting:
        if name not in self.__dict__:
            self.__dict__[name] = extend_json.getProperty(filePath=self._FILE, keys=(name, ))
        return self.__dict__[name]

    def __setattr__(self, name: str, value: Setting) -> Setting:
        self.__dict__[name] = value
        return value

    def save(self) -> int:
        counter = 0
        for name in self.__dict__:
            if extend_json.containsProperty(filePath=self._FILE, keys=(name, )):
                file_property = extend_json.getProperty(filePath=self._FILE, keys=(name, ))
                if not file_property == self.__dict__[name]:
                    extend_json.setProperty(filePath=self._FILE, keys=(name, ), value=self.__dict__[name])
                    counter += 1
        return counter
