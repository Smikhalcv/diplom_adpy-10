import requests
import json


class Info():
    """Получает информацию о пользователе с его страницы"""

    def __init__(self, user, parametr, access_token):
        self.user_id = user
        self.URL = 'https://api.vk.com/method/'
        self.fields = 'bdate,sex,city,interests,' + parametr
        self.token = access_token
        self.param = {
            'user_ids': self.user_id,
            'access_token': self.token,
            'v': 5.103,
            'fields': self.fields
        }

    def get_info(self):
        """Получает информацию о пользователе"""
        try:
            response = requests.get(f'{self.URL}users.get', params=self.param).json()['response'][0]
        except KeyError:
            print('Отсутвствует ключ "response", возможно устарел токен!')
        return response