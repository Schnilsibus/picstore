from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class Command(ABC):
    def __init__(self):
        ABC.__init__(self)

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def construct_parser(raw_parser: ArgumentParser) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def run(arguments: Namespace) -> None:
        raise NotImplementedError()
