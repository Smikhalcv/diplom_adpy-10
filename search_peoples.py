import datetime
import requests
from tqdm import tqdm

from User.get_info_user import Info
from mongo_db import Mongo_DB


class Search():
    '''Класс для поиска людей в вк'''

    # Получает данный для поиска исходя информации пользователя
    def __init__(self, token, user_id):
        self.user_id = user_id
        self.token = token
        #self.change_parametr()

    def change_parametr(self):
        # Изменяет по желанию критерии для поиска
        self.param_search = {
            'access_token': self.token,
            'sort': 1,
            'count': 1000,
            'v': 5.103,
        }
        print('''Желаете указать другие параметры для поиска? (да/нет)
Иначе критериями для поиска будет информация о пользователе''')
        # выполняет запросы для получения id города для поиска
        flag = input('- ')
        if flag.lower().startswith('д'):
            self.parametr = self.get_parametr()
            info = Info(self.user_id, self.parametr, self.token)
            user_info = info.get_info()
            self.info = user_info
            self.fields = info.fields + self.parametr
            self.sex = self.info['sex']
            if self.sex == 1:
                self.param_search['sex'] = 2
            elif self.sex == 2:
                self.param_search['sex'] = 1
            try:
                self.param_search['city'] = self.get_city()
            except IndexError:
                self.param_search['city'] = self.info['city']['id']
            self.get_age()
            self.get_range()
        else:
            self.parametr = ''
            info = Info(self.user_id, self.parametr, self.token)
            user_info = info.get_info()
            self.info = user_info
            self.fields = info.fields + self.parametr
            self.sex = self.info['sex']
            if self.sex == 1:
                self.param_search['sex'] = 2
            elif self.sex == 2:
                self.param_search['sex'] = 1
            b = datetime.datetime.now()
            dt = datetime.datetime.strptime(self.info['bdate'], '%d.%m.%Y')
            self.age = round((b - dt).days / 365)
            self.range = range
            self.param_search['city'] = self.info['city']['id']

    def get_parametr(self):
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
        print('''Укажите пустой параметр, если закончили перечисление или доп. параметр не нужен.
(если не знаете что ввести введите help, для отображения команд)''')
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

    def get_city(self):
        param_id_city = {'access_token': self.token,
                         'v': 5.103,
                         }
        print('Укажите страну для поиска. Россия - 1, Украина - 2, Беларусь - 3')
        while True:
            try:
                country_id = int(input('- '))
                break
            except ValueError:
                continue
        if str(country_id) in ['1', '2', '3']:
            print('Укажите город для поиска')
            city = input()
            param_id_city['country_id'] = country_id
            param_id_city['q'] = city
        response = requests.get('https://api.vk.com/method/database.getCities', params=param_id_city).json()
        return response['response']['items'][0]['id']

    def get_age(self):
        print('Укажите возраст кандидатов для поиска:')
        while True:
            try:
                self.age = int(input('- '))
                break
            except ValueError:
                continue

    def get_range(self):
        print('Укажите погрешность возраст для поиска:')
        while True:
            try:
                self.range = int(input('- '))
                break
            except ValueError:
                continue

    def search_vk(self):
        """Функция запроса поиска"""
        peoples = requests.get('https://api.vk.com/method/users.search', params=self.param_search).json()['response']
        return peoples

    def friends_groups_user(self, users_id):
        """Формирует функцию для получения групп и друзей по id"""
        code = '''return [ API.friends.get({
            'user_id': %s,
            "v": "5.103"
        }),
         API.groups.get({
            'user_id': %s,
            "v": "5.103"
        })];''' % (users_id, users_id)

        response = requests.post(
            url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": self.token,
                "v": "5.103"
            }
        )
        return response.json()

    def compability(self):
        """Ядро программы, выполняющее сортировку людей по их совместимости с пользователем"""

        value_compability = {}
        interests_user = []
        try:
            friends_user, groups_user = self.friends_groups_user(self.user_id)['response']
        except KeyError:
            friends_user = []
            groups_user = []
        try:
            list_friends_user = friends_user['items']
        except TypeError:
            list_friends_user = []
        except KeyError:
            list_friends_user = []
        try:
            list_groups_user = groups_user['items']
        except TypeError:
            list_groups_user = []
        except KeyError:
            list_groups_user = []
        if 'interests' in self.info.keys():
            for interests in self.info['interests']:
                interests_user.append(interests.lower().strip())  # получает список интересов пользователя из его данных
        for people in tqdm(self.search_vk()['items'], ncols=100):  # Начисляет баллы совместимости
            count_compability = 0
            try:
                friends_people, groups_people = self.friends_groups_user(people['id'])['response']
            except KeyError:
                friends_people = []
                groups_people = []
            list_friends_people = []
            list_groups_people = []
            try:
                list_friends_people = friends_people['items']
            except TypeError:
                pass
            try:
                list_groups_people = groups_people['items']
            except TypeError:
                pass
            if list_friends_people and list_friends_user:  # сравнивает друзей человека и пользователя, за каждого друга +3 к совместимости
                for friend in list_friends_user:
                    if friend in list_friends_people:
                        count_compability += 3
            if list_groups_people and list_groups_user:  # сравнивает группы человека и пользователя, за каждую группу +2 к совместимости
                for group in list_groups_user:
                    if group in list_groups_people:
                        count_compability += 2
            if 'bdate' in people.keys():  # Считает возраст человека и сравнивает его с возрастом пользователя
                if len(people['bdate']) > 5:  # В зависимости от разницы начисляет баллы
                    bdate_people = datetime.datetime.strptime(people['bdate'], '%d.%m.%Y')
                    age_people = round((datetime.datetime.now() - bdate_people).days / 365)
                    if abs(age_people - self.age) == 0:
                        count_compability += 5
                    elif abs(age_people - self.age) == 1:
                        count_compability += 4
                    elif abs(age_people - self.age) == 2:
                        count_compability += 3
                    elif abs(age_people - self.age) >= 3:
                        count_compability += 2
            if 'interests' in people.keys():  # сравнивает интересы человека и пользователя
                if people['interests']:
                    interests_people = []
                    for interests in people['interests']:
                        interests_people.append(interests.lower().strip())
                    for interests in interests_user:
                        if interests in interests_people:
                            count_compability += 0.5
            value_compability[people['id']] = count_compability  # Формирует словарь id - совместимость
            # Преобразует из словаря совместимости список id людей отсортированных согласно их совместимости
            full_list_value_compability = sorted(value_compability.values())
            full_list_value_compability.reverse()
            list_key = []
            for item in full_list_value_compability:
                for key, value in value_compability.items():
                    if item == value and key not in list_key:
                        list_key.append(key)
                        break
        # Преобразует список совместимости в словарь, для занесения его в дб, предварительно
        # удаляя старый документ
        dict_sort_id_compability = {}
        dict_sort_id_compability[f'{str(self.user_id)}'] = list_key
        data = []
        data.append(dict_sort_id_compability)
        database = Mongo_DB('VKinder')
        database.create_db()
        database.create_coll(f'cache {str(self.user_id)}')
        database.del_doc_coll()
        database.input_data_many(data)


if __name__ in '__main__':
    token = 'de7123bbc443c6bc68d0a839aaa0cfcaf61f73c1e55ef1d006358b38066d5a86806b1225ebabee8283ea6'
    user = Search(token, '112863023')
    # pprint(user.search_vk())
    print(user.compability())
