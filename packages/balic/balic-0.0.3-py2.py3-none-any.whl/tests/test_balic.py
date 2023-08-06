import unittest

from balic import Balic


class TestBalic(unittest.TestCase):
    def setUp(self):

        self.balic = Balic("test")

    def test_balic_init(self):

        self.assertIn("lxc_dir", self.balic.__config__)
