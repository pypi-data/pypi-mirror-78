import unittest

from mappa_api.services import EscotistaService, MAPPAService


class TestEscotistaService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mappa = MAPPAService()
        cls.login = cls.mappa.login('guionardo', 'A1GU')
        cls.svc = EscotistaService(cls.mappa)

    def test_get_user_info(self):
        self.assertTrue(self.login.is_valid)
        user_info = self.svc.get_user_info(self.login)
        self.assertIsNotNone(user_info)

    def test_secoes(self):
        self.assertTrue(self.login.is_valid)
        secoes = self.svc.get_secoes(self.login)
        self.assertIsNotNone(secoes)
        equipe = self.svc.get_equipe(self.login, secoes[0].codigo)
        self.assertIsNotNone(equipe)
        marcacoes = self.svc.get_marcacoes(self.login, secoes[0].codigo)
        self.assertIsNotNone(marcacoes)
