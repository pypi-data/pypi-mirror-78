from abc import ABC, abstractmethod
import argparse


class Shell(ABC):

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command", help="select one of the different commands ", choices=[c.name for c in self.get_commands()])
        parser.add_argument("subcommand", nargs='?', help="specify a subcommand")
        args = parser.parse_args()
        command = next(iter([c for c in self.get_commands() if c.name == args.command]), None)

        if command:
            command.run(args)
        else:
            print("{0} is not a valid command".format(args.command))


    @abstractmethod
    def get_commands(self):
        return []

