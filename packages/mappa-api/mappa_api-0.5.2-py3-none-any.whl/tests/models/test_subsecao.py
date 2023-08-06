import unittest

from mappa_api.models.mappa.subsecao import Subsecao

from .tools import read_response


class TestSubsecao(unittest.TestCase):

    def setUp(self):
        self.model = read_response('subsecao.json')

    def test_subsecao(self):
        subsecao = Subsecao(**self.model)
        self.assertEqual(subsecao.codigo, 5649)
        self.assertEqual(len(subsecao.associados), 5)
