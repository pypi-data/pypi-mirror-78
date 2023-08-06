import os
import sys
import inspect
import importlib.util
from argparse import ArgumentParser, REMAINDER


class Command:
    """Base class for CLI commands
    You should override at least run() method
        run() - method is being called to do the main job
        init_argument_parser(parser) - override this method if you want to accept arguments
        NAME - if this property is not None it is used as command name.
               Otherwise command name is generated from class name
        DESCRIPTION - description that is used in help messages. Consider setting it to something meaningful.
    """
    NAME = None
    DESCRIPTION = None
    NO_ARGPARSE = False

    def __init_subclass__(cls, **kwargs):
        if cls.NAME is None:
            cls.NAME = cls.__name__.lower()

    def __init__(self, app):
        self.app = app
        if self.NAME is None:
            self.NAME = self.__class__.__name__.lower()
        if self.DESCRIPTION is None:
            self.DESCRIPTION = '"%s" has no DESCRIPTION' % (self.NAME,)
        self.args = None
        self.raw_args = None

    def init_argument_parser(self, parser):
        """
        This method is called to configure argument subparser for command
        Override it if you need to accept arguments
          - parser: argparse.ArgumentParser to fill with arguments
        """

    def run(self):
        """
        This is a main method of command. Override it and do all the job here
        Command arguments can be read from self.args
        The return value from this method will be used as CLI exit code
        """
        raise NotImplementedError()


def is_a_command_class(obj):
    return inspect.isclass(obj) and issubclass(obj, Command) and obj != Command


def load_commands():
    commands = {}
    for mod_pref in ["glasskit.commands", "commands"]:
        commands_package = importlib.util.find_spec(mod_pref).origin
        for pyfile in os.listdir(os.path.dirname(commands_package)):
            if pyfile.endswith(".py"):
                module_name = f"{mod_pref}.{pyfile[:-3]}"
                module = importlib.import_module(module_name)
                for cls_name in dir(module):
                    cls = getattr(module, cls_name)
                    if is_a_command_class(cls):
                        commands[cls.NAME] = cls
    return commands


def main(app):

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(
        title='Commands',
        help="One of the following commands",
        description='use <command> --help to get help on particular command',
        metavar="<command>",
    )

    for cmd_name, cmd_class in load_commands().items():
        command = cmd_class(app)
        if command.NO_ARGPARSE:
            command_parser = subparsers.add_parser(
                command.NAME,
                help=command.DESCRIPTION,
                add_help=False,
                # Ugly hack to prevent arguments from being parsed as options
                prefix_chars=chr(0),
            )
            command_parser.add_argument('raw_args', nargs=REMAINDER)
        else:
            command_parser = subparsers.add_parser(
                command.NAME, help=command.DESCRIPTION)
        command_parser.set_defaults(command=command)
        command.init_argument_parser(command_parser)

    args = parser.parse_args()
    if not hasattr(args, "command"):
        print(f"Usage: {sys.argv[0]} <command> [<options>]")
    else:
        args.command.args = args
        if 'raw_args' in args:
            args.command.raw_args = args.raw_args
        return args.command.run()
