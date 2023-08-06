import logging

from cliff.command import Command
from balic import Balic


class Create(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Create a new linux container.
        """
        self.balic = Balic(parsed_args.name)
        self.balic.create()

    def get_description(self):
        return "create linux container"

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        return Balic.get_parser(parser)
