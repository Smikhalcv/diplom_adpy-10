import requests
import webbrowser
import re
from mongo_db import Mongo_DB
from datetime import datetime


class Token():
    """Получает токен, открывает браузер по умолчанию, для авторизации,
    из строки полченного урла извлекает токен"""

    def __init__(self):
        self.URL = 'https://oauth.vk.com/authorize'
        self.APP_ID = '7321296'
        self.param = {
            'v': 5.103,
            'client_id': self.APP_ID,
            'display': 'page',
            'scope': 'manage,photos,docs,stories,wall',
            'response_type': 'token'
        }
        self.database = Mongo_DB('VKinder')
        self.database.create_db()
        self.database.create_coll('Access_token')
        self.time_now = datetime.now()

    def create_token(self):
        """выполняет запрос, для получения токена и открывает его в браузере по умолчанию"""
        request = requests.get(self.URL, params=self.param)
        webbrowser.open_new(request.url)
        # Выполняет запрос строки, пока не будет введён урл
        while True:
            print('''Скопируйте сюда строку полученного URL из адресной строки браузера, 
после подтверждения прав.''')
            token = input('''(ВНИМАНИЕ!!! после ссылки нажмите пробел)
- ''')
            pattern = re.compile('\S*access_token=(\S{85})\S*\s*')
            new_pattern = r'\1'
            ACCESS_TOKEN = pattern.sub(new_pattern, token)
            if len(ACCESS_TOKEN) == 85:
                ACCESS_TOKEN = ACCESS_TOKEN
                break
            else:
                print('Неправильно введена ссылка')
        return ACCESS_TOKEN

    def write_token(self):
        """Записывает токен в БД и время его получения"""
        dict_token_time = {}
        dict_token_time['time'] = self.time_now
        dict_token_time['token'] = self.create_token()
        self.database.del_doc_coll()
        self.database.input_data(dict_token_time)
        self.database.read()
        self.time_token = self.database.data[0]['time']
        return dict_token_time['token']

    def read_token(self):
        """Читает токен из БД, если с его получения прошло более суток, получает новый токен и переписывает его в БД"""
        try:
            self.database.read()
            self.time_token = self.database.data[0]['time']
        except IndexError:
            self.write_token()
        if (self.time_now - self.time_token).days >= 1:
            self.write_token()
        else:
            return self.database.data[0]['token']


if __name__ in '__main__':
    token = Token()
    access_token = token.read_token()
    print(access_token)
