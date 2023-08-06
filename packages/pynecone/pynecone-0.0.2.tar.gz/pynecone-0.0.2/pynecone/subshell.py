from abc import ABC
from .shell import Shell
from .command import Command


class Subshell(Shell, Command, ABC):

    def __init__(self, name):
        super().__init__(name)

    def run(self, args):
        command = next(iter([c for c in self.get_commands() if c.name == args.subcommand]), None)

        if command:
            command.run(args)
        else:
            print("{0} is not a valid command".format(args.subcommand))
