import requests

from User.get_token import Token
from User.user_id import id_user
from search_peoples import Search


def get_parametr():
    '''Преобразует дополнительные параметры для поиска в строку, необходимую для запроса'''

    str_parametr = 'photo_id, verified, sex, bdate, city, country, home_town, online, domain, has_mobile, contacts, site, education, ' \
                   'universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, ' \
                   'personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, ' \
                   'can_see_all_posts, can_see_audio, ' \
                   'can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, ' \
                   'maiden_name, crop_photo, ' \
                   'is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group'
    list_access_parametr = []
    for i in (str_parametr + ', help').split(','):
        list_access_parametr.append(i.strip())
    print('''Укажите другие необходимые параметры или пустой параметр, если закончили перечисление или доп. параметр не нужен.
    (уже введены день рождение, пол, город, интересы; если не знаете что ввести введите help, для отображения команд)''')
    input_parametr = True
    list_parametr = []
    while input_parametr:  # Просит вводить параметр до тех пор, пока не будет введён пустой
        input_parametr = input('- ')  # и добавляет его в список, кроме help, который потом переделывает в строку
        if input_parametr in list_access_parametr:
            if input_parametr == 'help':
                print('''Доступные значения: photo_id, verified, sex, bdate, city, country, home_town,
            online, domain, has_mobile, contacts, site, education, universities, schools, status,
            last_seen, followers_count, common_count, occupation, nickname, relatives, relation,
            personal, connections, exports, activities, interests, music, movies, tv, books,
            games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message,
            can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo,
            is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group.''')
            else:
                list_parametr.append(input_parametr)
    parametr = ','.join(list_parametr)
    return parametr


def get_result(dict_info, token):
    '''Получается словарь где ключ это id человека, а значение - степень его совместимости,
    преобразует его и выводит первых 10 человек с наибольшей совместимостью'''

    # Сортирует полученный словарь по значениям
    full_list_value_compability = sorted(dict_info.values())
    full_list_value_compability.reverse()
    list_value_compability = full_list_value_compability[:10]
    list_key = []
    # Сравнивает значение совместимости со значениями в словаре
    # Получается список id 10 топовых людей и удаляет их из получнного словаря
    for item in list_value_compability:
        for key, value in dict_info.items():
            if item == value and key not in list_key:
                list_key.append(key)
                break
    for i in list_key:
        dict_info.pop(i)
    str_code = ''
    # Выполняет екзекьют запрос в апи вк, для 10 человек для получения их фотографий профиля
    for i in list_key:
        str_code += """API.photos.get({'owner_id': %s,'album_id': 'profile','extended': 1,'count': 50}), """ % i
    code = 'return [%s];' % str_code
    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": token,
            "v": "5.103"
        }
    ).json()
    list_photo = []
    # Сортирует список фотографий по лайкам и выбирает топ-3, полученный данные вносит в список словарей,
    # где лежат ссылка на профиль человека и ссылки на топ3 его фотографий профиля
    for i in response['response']:
        photo_dict = {}
        data = {}
        for y in i['items']:
            photo_dict[y['likes']['count']] = y['sizes'][-1]['url']
            data['url_id'] = f'https://vk.com/id{y["owner_id"]}'
        sortering = list(photo_dict.keys())
        sortering = sorted(sortering)
        sortering.reverse()
        sortering = sortering[:3]
        data['url_photo'] = []
        for l in sortering:
            data['url_photo'].append(photo_dict[l])

        list_photo.append(data)

    return list_photo, dict_info


if __name__ in '__main__':
    token = Token()
    token = token.create_token()
    user_id = id_user(token)
    parametr = get_parametr()
    user = Search(token, user_id, parametr)
    value_compability = user.compability()
    print('''Для получения топ-10 самым совместимых людей, введите search или s
    (При повторном ввое команды, ввыведутся следующий топ-10 людей);
Для выхода введите quit или q;
Введите команду: ''')
    while True:
        event = input('- ')
        if event.lower() in ('search', 's'):
            list_photo, value_compability = get_result(value_compability, token)
            print(list_photo)
        if event.lower() in ('quit', 'q'):
            break
