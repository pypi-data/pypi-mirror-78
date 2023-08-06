import unittest
from datetime import datetime

from mappa_api.models.mappa.login import Login

from .tools import read_response


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.model = read_response('login.json')

    def test_login(self):
        login = Login(**self.model)
        self.assertEqual(login.userId, 50442)

    def test_valid_login(self):
        model = {
            "id": "a",
            "ttl": 1000,
            "created": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "userId": 1
        }
        login = Login(**model)
        self.assertTrue(login.is_valid)
