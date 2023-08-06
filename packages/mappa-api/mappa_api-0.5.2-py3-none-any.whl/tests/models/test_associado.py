import unittest

from mappa_api.models.mappa.associado import Associado

from .tools import read_response


class TestAssociadoModel(unittest.TestCase):

    def setUp(self):
        self.model = read_response('associado.json')

    def test_associado(self):
        try:
            associado = Associado(**self.model)
            self.assertEqual(associado.codigo, 850829)
        except Exception as exc:
            self.fail(str(exc))
