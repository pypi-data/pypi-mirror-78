import logging

from cliff.command import Command
from balic import Balic


class Build(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Build and pack up a new linux container.
        """
        self.balic = Balic(parsed_args.name)
        self.balic.build(
            parsed_args.directory,
            parsed_args.output_file
        )

    def get_description(self):
        return "build and pack up a new linux container"

    def get_parser(self, prog_name):
        parser = super(Build, self).get_parser(prog_name)
        parser = Balic.get_parser(parser)
        parser.add_argument("-d", "--directory")
        parser.add_argument("-o", "--output-file")
        return parser
