from abc import ABC, abstractmethod
import argparse


class Command(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def add_arguments(self, parser):
        pass

    @abstractmethod
    def run(self, args):
        pass

    @abstractmethod
    def get_help(self):
        return None

    def setup(self, subparsers):
        parser = subparsers.add_parser(self.name, help=self.get_help())
        self.add_arguments(parser)
        return parser
