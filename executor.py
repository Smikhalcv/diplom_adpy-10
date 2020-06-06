import requests
import json
from mongo_db import Mongo_DB


def write_read_DB(user_id):
    '''Получается словарь из БД, где ключ это id человека, а значение - степень его совместимости,
        преобразует его и выводит первых 10 человек с наибольшей совместимостью
        переписывает БД новыми данными, обновляя их'''
    database = Mongo_DB('VKinder')
    database.create_db()
    database.create_coll(f'cache {user_id}')
    database.read()
    list_for_photo = database.data[0][user_id][:10]  # 10 человек наиболее совместимых
    list_id = database.data[0][user_id][10:]  # Оставшиеся люди из поиска
    print(list_for_photo)
    dict_id = {}
    dict_id[f'{user_id}'] = list_id
    list_dict_id = []
    list_dict_id.append(dict_id)
    database.del_doc_coll()
    database.input_data_many(list_dict_id)  # вносит оставшихся людей в колеекцию cache id для дальнейшей работы
    database.create_coll(f'{user_id}')
    dict_photo = {}
    dict_photo[f'{user_id}'] = list_for_photo
    database.del_doc_coll()
    list_dict_photo = []
    list_dict_photo.append(dict_photo)
    database.input_data_many(list_dict_photo)  # вносит id 10 человек, которые будут выведены пользователю
    return list_for_photo


def get_result(token, user_id):
    """Выполняет execute запрос, получая фото профилей топ-10, сортирует фото и выбирает из них топ-3
    создаёт файл с результатом"""
    list_for_photo = write_read_DB(user_id)
    str_code = ''
    # Выполняет execute запрос в апи вк, для 10 человек для получения их фотографий профиля
    for i in list_for_photo:
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
        if i['items']:
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
    with open(f'Result\\{user_id}.json', 'w', encoding='utf-8') as file:
        json.dump(list_photo, file, ensure_ascii=False, indent=2)
    print(f'Файл {user_id}.json с топ 10 пользователей создан в папке Result!')


if __name__ in '__main__':
    token = '1bca69ca0df3140a3a742fac61562fb6db21b434ba5a62929984b3d15c190bfd9710e2ce56326e823dfe6'
    user = '38309546'
    get_result(token, user)
