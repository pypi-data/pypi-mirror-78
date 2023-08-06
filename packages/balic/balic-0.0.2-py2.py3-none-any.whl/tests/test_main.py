import sys
import unittest

from balic.main import main


class TestMain(unittest.TestCase):
    def test_main(self):

        sys.argv = ["ls"]
        test_ls = main(argv=sys.argv[1:])
