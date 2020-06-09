import unittest
from unittest.mock import patch

import User.get_token


class Test_Token(unittest.TestCase):

    def setUp(self) -> None:
        self.url = 'https://oauth.vk.com/blank.html#access_token' \
                   '=917abda6333fef0ba798301198a5c21ccbcae3a487cf60dd6e29849551cfa8892b568e2bd7294fe063b7c&expires_in=86400&user_id=112863023'
        self.access_token = '917abda6333fef0ba798301198a5c21ccbcae3a487cf60dd6e29849551cfa8892b568e2bd7294fe063b7c'

    def test_create_token(self):
        with patch('User.get_token.input', return_value=self.url):
            test_token = User.get_token.Token()
            result = test_token.create_token()
            self.assertEqual(result, self.access_token)

    def test_write_token(self):
        with patch('User.get_token.input', return_value=self.url):
            test_token = User.get_token.Token()
            result = test_token.write_token()
            self.assertEqual(len(result), 85)
            self.assertEqual(type(result), str)

    def test_read_token(self):
        with patch('User.get_token.input', return_value=self.url):
            test_token = User.get_token.Token()
            result = test_token.read_token()
            self.assertEqual(len(result), 85)
            self.assertEqual(type(result), str)


if __name__ == '__main__':
    unittest.main()
