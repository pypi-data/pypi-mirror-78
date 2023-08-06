import logging

from cliff.command import Command
from balic import Balic


class Destroy(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Destroy linux container.
        """
        self.balic = Balic(parsed_args.name)
        self.balic.destroy()

    def get_description(self):
        return "destroy linux container"

    def get_parser(self, prog_name):
        parser = super(Destroy, self).get_parser(prog_name)
        return Balic.get_parser(parser)
