import unittest

from mappa_api.services.mappa_service import MAPPAService


class TestMAPPAService(unittest.TestCase):

    def setUp(self):
        self.svc = MAPPAService()

    def test_login(self):
        login = self.svc.login('guionardo', 'A1GU')
        self.assertTrue(login.is_valid)
