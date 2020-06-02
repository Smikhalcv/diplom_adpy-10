import requests

def id_user(token):
    """Получает id пользователя из его screen_name или непосредственно id"""

    user_id = input('Укажите ID или screen_name пользователя, для которого будет выполняться поиск: ')
    try:
        id = int(user_id)
    except ValueError:
        param = {'screen_name': user_id,
                 'access_token': token,
                 'v': 5.103}
        id = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=param).json()['response']['object_id']
        return id
    else:
        return id


if __name__ in '__main__':
    token = '1bca69ca0df3140a3a742fac61562fb6db21b434ba5a62929984b3d15c190bfd9710e2ce56326e823dfe6'
    print(id_user(token))