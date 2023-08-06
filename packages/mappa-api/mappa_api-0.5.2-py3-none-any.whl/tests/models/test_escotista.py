import unittest

from mappa_api.models.mappa.escotista import Escotista

from .tools import read_response


class TestEscotista(unittest.TestCase):

    def setUp(self):
        self.model = read_response('escotista.json')

    def test_escotista(self):
        try:
            escotista = Escotista(**self.model)
            self.assertEqual(escotista.codigo, 50442)
        except Exception as exc:
            self.fail(str(exc))
