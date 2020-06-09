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
            resp = requests.get(f'{self.URL}users.get', params=self.param).json()['response'][0]
        except KeyError:
            print('Отсутвствует ключ "response", возможно устарел токен!')
        else:
            return resp


if __name__ in '__main__':
    id = 11111111111111111111111111111
    par = ''
    token = 'd021bd5d2c897fc6ae5b2fd4c2c222c372b6531c8b1305a0022430cedc80c8ef1eb09abbe248f7097ca75'
    user = Info(id, par, token)
    user.get_info()
