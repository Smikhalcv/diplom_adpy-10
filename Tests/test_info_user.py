import unittest
from unittest.mock import patch
import sys
from io import StringIO

from User.get_info_user import Info
from User.get_token import Token

class Test_info(unittest.TestCase):

    def setUp(self):
        self.id_user = '1'
        self.par = ''
        with patch('User.get_token'):
            new_token = Token()
            token = new_token.read_token()
        self.test_user = Info(self.id_user, self.par, token)

    def test_get_info_old_token(self):
        old_token = '406685f1faab8bbb98bc5863684ea830f977b56b8dd54585d9a028d179253bffb3b3d57ef84fb227599cf'
        test_user = Info(self.id_user, self.par, old_token)
        self.assertFalse(test_user.get_info())

    def test_get_info_new_token(self):
        self.assertEqual(type(self.test_user.get_info()), dict)

    def test_get_info_true(self):
        self.assertTrue(self.test_user.get_info())

    def test_get_info_not_error(self):
        self.assertNotIn('error', self.test_user.get_info().keys())