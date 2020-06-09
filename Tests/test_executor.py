import unittest
from unittest.mock import patch
import os

from executor import write_read_DB
from executor import get_result
from User.get_token import Token


class Test_executor(unittest.TestCase):
    """Тест работает, толкьо с существующей коллекцией"""

    def setUp(self) -> None:
        self.user_id = '112863023'
        with patch('User.get_token'):
            new_token = Token()
            self.accesse_token = new_token.read_token()

    def test_write_read_list(self):
        with patch('executor.write_read_DB'):
            fr = write_read_DB(self.user_id)
        self.assertEqual(type(fr), list)

    def test_write_read_true(self):
        with patch('executor.write_read_DB'):
            fr = write_read_DB(self.user_id)
        self.assertTrue(fr)

    def test_get_result(self):
        directory = 'D:\\adpy\\diplom\\Result'
        file = f'{self.user_id}.json'
        with patch('executor.get_result'):
            get_result(self.accesse_token, self.user_id)
        files = os.listdir(directory)
        self.assertIn(file, files)
