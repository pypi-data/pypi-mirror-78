import unittest

from src.models.mappa.grupo import Grupo

from .tools import read_response


class TestGrupo(unittest.TestCase):

    def setUp(self):
        self.model = read_response('grupo.json')

    def test_grupo(self):
        grupo = Grupo(**self.model)
        self.assertEqual(grupo.codigo, 1)
