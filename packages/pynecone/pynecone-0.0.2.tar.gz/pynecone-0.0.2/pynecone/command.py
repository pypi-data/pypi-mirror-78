from abc import ABC, abstractmethod


class Command(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self, args):
        pass
