import configparser
import os
from pathlib import Path
from typing import TypeVar, Generic, Type

T = TypeVar("T")


class StorageValue(Generic[T]):
    app_name: str = None
    name: str = None
    default_value: T = None
    type: Type[T] = None

    def __init__(self):
        self._storage_file = os.path.join(self.base_dir, f".{self.name}")
        if os.path.exists(self._storage_file):
            self._value = self.load_value()
        else:
            self._value = self.resolve_default_value()
            self.write_value()

    @property
    def base_dir(self):
        return os.path.join(Path.home(), self.app_name)

    def load_value(self) -> T:
        with open(self._storage_file, "rt") as file:
            content = file.read()
            return self.type(content) if self.type else content

    def write_value(self):
        if self._value is not None:
            with open(self._storage_file, "wt") as file:
                file.write(str(self._value))
        # ToDo: else delete file?

    def resolve_default_value(self) -> T:
        return self.default_value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value
        self.write_value()


class ConfigValue(StorageValue[configparser.ConfigParser]):

    def load_value(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(self._storage_file)
        return config
