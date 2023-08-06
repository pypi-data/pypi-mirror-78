from abc import ABC, abstractmethod
from .command import Command

import argparse


class Shell(Command, ABC):

    def run(self, args=None):
        if args is None:
            parser = argparse.ArgumentParser(prog=self.name)
            self.add_arguments(parser)

            subparsers = parser.add_subparsers(dest='command', help=self.get_help())

            for c in self.get_commands():
                c.setup(subparsers)
            args = parser.parse_args()

        print(args)

        if args.command:
            command = next(iter([c for c in self.get_commands() if c.name == args.command]), None)
            if command:
                if hasattr(args, 'subcommand'):
                    subcommand = next(iter([c for c in command.get_commands() if c.name == args.subcommand]), None)
                    if subcommand:
                        subcommand.run(args)
                    else:
                        print("{0} is not a valid subcommand".format(args.subcommand))
                else:
                    command.run(args)
            else:
                print("{0} is not a valid command".format(args.command))


    @abstractmethod
    def get_commands(self):
        return []

    def setup(self, subparsers):
        parser = super().setup(subparsers)
        commands = self.get_commands()
        if commands:
            subsubparsers = parser.add_subparsers(dest='subcommand')
            for c in commands:
                c.setup(subsubparsers)




