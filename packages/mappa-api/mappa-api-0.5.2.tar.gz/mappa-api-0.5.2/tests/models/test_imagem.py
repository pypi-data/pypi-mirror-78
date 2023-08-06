import unittest
from mappa_api.models.mappa.imagem import Imagem
from .tools import read_response


class TestImagem(unittest.TestCase):

    def setUp(self):
        self.model = read_response('imagem.json')

    def test_imagem(self):
        imagem = Imagem(**self.model)
        self.assertIsNotNone(imagem.imagem)
