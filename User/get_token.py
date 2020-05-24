import requests
import webbrowser
import re


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

    def create_token(self):

        request = requests.get(self.URL, params=self.param)

        webbrowser.open_new(request.url)
        # Выполняет запрос строки, пока не будет введён урл
        while True:
            print('''Скопируйте сюда строку полученного урла из адресной строки браузера, 
после поддверждения прав.''')
            token = input('''(ВНИМАНИЕ!!! после ссылки нажмите пробел)
- ''')
            pattern = re.compile('\S*access_token=(\S{85})\S*')
            new_pattern = r'\1'
            ACCESS_TOKEN = pattern.sub(new_pattern, token)
            if len(ACCESS_TOKEN) == 86:
                ACCESS_TOKEN = ACCESS_TOKEN[:-1]
                break

            else:
                print('Неправильно введена ссылка')

        return ACCESS_TOKEN


if __name__ in '__main__':
    User = Token()
    User.create_token()
