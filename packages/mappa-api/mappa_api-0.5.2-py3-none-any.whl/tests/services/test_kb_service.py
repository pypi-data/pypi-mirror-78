import unittest

from mappa_api.models.enums import Ramo
from mappa_api.services.kb_service import KBService, MAPPAService


class TestKBService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mappa = MAPPAService()
        cls.login = cls.mappa.login('guionardo', 'A1GU')
        cls.svc = KBService(cls.mappa)

    def test_get_progressoes(self):
        self.assertTrue(self.login.is_valid)
        prg_alcateia = self.svc.get_progressoes(self.login, Ramo.Alcateia)
        self.assertIsNotNone(prg_alcateia)

    def test_get_especialidades(self):
        self.assertTrue(self.login.is_valid)
        esp = self.svc.get_especialidades(self.login)
        self.assertIsNotNone(esp)
