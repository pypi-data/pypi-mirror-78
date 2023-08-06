import unittest

from mappa_api.models.mappa.secao import Secao

from .tools import read_response


class TestSecao(unittest.TestCase):

    def setUp(self):
        self.model = read_response('secao.json')

    def test_secao(self):
        secao = Secao(**self.model)
        self.assertEqual(secao.codigo, 1538)
