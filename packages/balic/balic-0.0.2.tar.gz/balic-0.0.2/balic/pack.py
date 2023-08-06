import os
import logging

from cliff.command import Command
from balic import Balic


class Pack(Command):

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        """Pack linux container as rootfs.tar.gz
        """
        output_file = os.path.abspath(os.path.expanduser(parsed_args.output_file))

        self.balic = Balic(parsed_args.name)

        self.balic.pack(output_file)

    def get_description(self):
        return "pack linux container"

    def get_parser(self, prog_name):
        parser = super(Pack, self).get_parser(prog_name)
        parser = Balic.get_parser(parser)
        parser.add_argument("-o", "--output-file")
        return parser
