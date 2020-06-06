import requests


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


if __name__ in '__main__':
    id = 12684534564312
    par = ''
    token = '406685f1faab8bbb98bc5863684ea830f977b56b8dd54585d9a028d179253bffb3b3d57ef84fb227599cf'
    user = Info(id, par, token)
    print(user.get_info())
