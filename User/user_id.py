import requests


def id_user(token):
    """Получает id пользователя из его screen_name или непосредственно id"""
    while True:
        user_id = input('Укажите ID или screen_name пользователя, для которого будет выполняться поиск: ')
        param = {'screen_name': user_id,
                 'access_token': token,
                 'v': 5.103}
        try:
            id = int(user_id)
        except ValueError:
            id = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=param).json()
            if id['response']:
                if id['response']['type'] == 'user':
                    return id['response']['object_id']
            print('Неправильно ввели screen_name/id или такого пользователя не существует.')
        else:
            url = 'https://api.vk.com/method/user.get'
            request = requests.get(url, param).json()
            if 'error' not in request.keys():
                return id
            else:
                print('Пользователя с таким id не существует.')


if __name__ in '__main__':
    token = '406685f1faab8bbb98bc5863684ea830f977b56b8dd54585d9a028d179253bffb3b3d57ef84fb227599cf'
    print(id_user(token))
