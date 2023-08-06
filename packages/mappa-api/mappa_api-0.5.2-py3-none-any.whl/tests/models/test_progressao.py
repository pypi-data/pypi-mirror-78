import unittest

from mappa_api.models.mappa.progressao import Progressao

from .tools import read_response


class TestProgressao(unittest.TestCase):

    def setUp(self):
        self.model = read_response('progressao.json')

    def test_progressao(self):
        progressao = Progressao(**self.model)
        self.assertEqual(progressao.codigo, 1)
