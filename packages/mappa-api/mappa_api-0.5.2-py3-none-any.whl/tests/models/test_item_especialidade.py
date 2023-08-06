import unittest

from mappa_api.models.mappa.item_especialidade import ItemEspecialidade

from .tools import read_response


class TestItemEspecialidade(unittest.TestCase):

    def setUp(self):
        self.model = read_response('item_especialidade.json')

    def test_grupo(self):
        item = ItemEspecialidade(**self.model)
        self.assertEqual(item.id, 1)
