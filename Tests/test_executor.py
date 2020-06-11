import unittest
from unittest.mock import patch
import os

from executor import write_read_DB
from executor import get_result
from User.get_token import Token
from mongo_db import Mongo_DB


class Test_executor(unittest.TestCase):
    """Тест проверят формат полученных данных из БД, их наличие, и запись файла"""

    def setUp(self) -> None:
        database = Mongo_DB('VKinder')
        database.create_db()
        dict_data = {}
        dict_data['1'] = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
        test_data = []
        test_data.append(dict_data)
        database.create_coll('1')
        database.input_data_many(test_data)
        database.del_doc_coll()
        database.create_coll('cache 1')
        database.del_doc_coll()
        database.input_data_many(test_data)
        with patch('User.get_token'):
            new_token = Token()
            self.accesse_token = new_token.read_token()

    def test_write_read_list(self):
        with patch('executor.write_read_DB'):
            fr = write_read_DB('1')
        self.assertEqual(type(fr), list)

    def test_write_read_true(self):
        with patch('executor.write_read_DB'):
            fr = write_read_DB('1')
        self.assertTrue(fr)

    def test_get_result(self):
        directory = 'D:\\adpy\\diplom\\Result'
        file = '1.json'
        with patch('executor.get_result'):
            get_result(self.accesse_token, '1')
            files = os.listdir(directory)
        self.assertIn(file, files)
