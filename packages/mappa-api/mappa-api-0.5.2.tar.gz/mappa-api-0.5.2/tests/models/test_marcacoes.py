import unittest

from mappa_api.models.mappa.marcacoes import Marcacoes

from .tools import read_response


class TestMarcacoes(unittest.TestCase):

    def setUp(self):
        self.model = read_response('marcacoes.json')

    def test_marcacoes(self):
        marcacoes = Marcacoes(**self.model)
        self.assertEqual(marcacoes.dataHora.day, 14)
        self.assertEqual(len(marcacoes.values), 2656)
