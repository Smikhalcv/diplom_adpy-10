import requests

def id_user(token):
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