import os
import logging

from cliff.command import Command
from balic import Balic


class Build(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Build linux container
        """
        directory = os.path.abspath(os.path.expanduser(parsed_args.directory))

        self.balic = Balic(parsed_args.name)

        self.balic.build(directory)

    def get_description(self):
        return "build linux container"

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser = Balic.get_parser(parser)
        parser.add_argument("-d", "--directory")
        return parser
