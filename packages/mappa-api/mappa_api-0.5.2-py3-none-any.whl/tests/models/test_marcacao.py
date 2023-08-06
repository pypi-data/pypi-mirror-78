import unittest

from mappa_api.models.mappa.marcacao import Marcacao

from .tools import read_response


class TestMarcacao(unittest.TestCase):

    def setUp(self):
        self.model = read_response('marcacao.json')

    def test_marcacao(self):
        try:
            marcacao = Marcacao(**self.model)
            self.assertEqual(marcacao.codigoAssociado, 973211)
        except Exception as exc:
            self.fail(str(exc))
