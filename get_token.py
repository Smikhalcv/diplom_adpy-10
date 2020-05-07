import requests
import webbrowser
import re

def create_token():
    URL = 'https://oauth.vk.com/authorize'
    APP_ID = '7321296'
    param = {
        'v': 5.103,
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'manage,photos,docs,stories,wall',
        'response_type': 'token'
    }

    request = requests.get(URL, params=param)

    webbrowser.open_new(request.url)

    while True:
        print('''Скопируйте сюда строку полученного урла из адресной строки браузера, 
после поддверждения прав.''')
        token = input('''(после ссылки нажмите пробел)
- ''')
        # if len(token) >= 98:
        pattern = re.compile('\S*access_token=(\S{85})\S*')
        new_pattern = r'\1'
        ACCESS_TOKEN = pattern.sub(new_pattern, token)
        if len(ACCESS_TOKEN) == 86:
            break

        else:
            print('Неправильно введена ссылка')

    return ACCESS_TOKEN

if __name__ in '__main__':
    print(create_token())