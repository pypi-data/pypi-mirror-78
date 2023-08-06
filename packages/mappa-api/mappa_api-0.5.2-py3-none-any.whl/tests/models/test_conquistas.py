import unittest

from mappa_api.models.mappa.conquistas import Conquistas

from .tools import read_response


class TestConquistas(unittest.TestCase):

    def setUp(self):
        self.model = read_response('conquistas.json')

    def test_conquistas(self):
        conquistas = Conquistas(**self.model)
        self.assertEqual(len(conquistas.values), 93)
