import requests
import json

#from User.get_token import Token

# token = Token()
# ACCESS_TOKEN = token.create_token()
# #print(ACCESS_TOKEN)

class Info():

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

        #self.fields += self.parametr
        try:
            response = requests.get(f'{self.URL}users.get', params=self.param).json()['response'][0]
        except KeyError:
            print('Отсутвствует ключ "response", возможно устарел токен!')

        return response

    def json_info(self):
        try:
            response = requests.get(f'{self.URL}users.get', params=self.param).json()['response'][0]
        except KeyError:
            print('Отсутвствует ключ "response", возможно устарел токен!')

        with open(f'Cache\\{self.user_id}-info.json', 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=2)
