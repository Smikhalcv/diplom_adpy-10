import unittest
from unittest.mock import patch

import search_peoples
from User.get_token import Token
from mongo_db import Mongo_DB

class Test_search(unittest.TestCase):

    def setUp(self) -> None:
        self.user_id = '1'
        with patch('User.get_token'):
            new_token = Token()
            self.accesse_token = new_token.read_token()
        self.test_user = search_peoples.Search(self.accesse_token, self.user_id)


    def test_get_parametr_str(self):
        with patch('search_peoples.input', side_effect=['movies', '']):
            test_data = self.test_user.get_parametr()
        self.assertEqual(type(test_data), str)

    def test_get_parametr_true(self):
        with patch('search_peoples.input', side_effect=['movies', '']):
            test_data = self.test_user.get_parametr()
        self.assertTrue(test_data)

    def test_get_city_true(self):
        with patch('search_peoples.input', side_effect=['3', 'жлобин']):
            test_data = self.test_user.get_city()
        self.assertTrue(test_data)

    def test_get_city_int(self):
        with patch('search_peoples.input', side_effect=['3', 'жлобин']):
            test_data = self.test_user.get_city()
        self.assertEqual(type(test_data), int)

    def test_search_vk_dict(self):
        with patch('search_peoples.input', return_value='нет'):
            self.test_user.change_parametr()
        test_data = self.test_user.search_vk()
        self.assertEqual(type(test_data), dict)

    def test_search_vk_true(self):
        with patch('search_peoples.input', return_value='нет'):
            self.test_user.change_parametr()
        test_data = self.test_user.search_vk()
        self.assertTrue(test_data)

    def test_friends_groups_user_dict(self):
        test_data = self.test_user.friends_groups_user(self.user_id)
        self.assertEqual(type(test_data), dict)

    def test_friends_groups_user_true(self):
        test_data = self.test_user.friends_groups_user(self.user_id)
        self.assertTrue(test_data)

    def test_compability(self):
        database = Mongo_DB('VKinder')
        database.create_db()
        test_inf = f'cache {str(self.user_id)}'
        with patch('search_peoples.input', return_value='нет'):
            self.test_user.change_parametr()
        self.test_user.compability()
        self.assertIn(test_inf, database.show_coll())