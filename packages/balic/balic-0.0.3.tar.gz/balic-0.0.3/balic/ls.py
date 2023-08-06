import logging

from cliff.command import Command
from balic import Balic


class Ls(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """List linux containers.
        """
        self.balic = Balic(parsed_args.name)
        self.balic.ls(parsed_args.list_all)

    def get_description(self):
        return "list linux containers"

    def get_parser(self, prog_name):
        parser = super(Ls, self).get_parser(prog_name)
        parser.add_argument("-a", "--all", dest="list_all", action="store_true")
        parser.set_defaults(list_all=False)
        return Balic.get_parser(parser)
