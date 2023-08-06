import unittest

from balic import Balic


class TestBalic(unittest.TestCase):
    def setUp(self):

        self.balic = Balic()

    def test_balic_init(self):

        self.assertIn("balic", self.balic.__config__)

    def test_balic_banner(self):

        banner = self.balic.banner(None, use_figlet=False)

        self.assertIn("Balic v", banner)
