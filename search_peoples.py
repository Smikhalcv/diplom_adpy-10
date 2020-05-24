import datetime
import requests
import json
from tqdm import tqdm

from User.get_info_user import Info


class Search():
    '''Класс для поиска людей в вк'''

    # Получает данный для поиска исходя информации пользователя
    def __init__(self, token, user_id, parametr='', range=2):
        self.user_id = user_id
        info = Info(self.user_id, parametr, token)
        user_info = info.get_info()
        self.info = user_info
        self.city_id = self.info['city']['id']
        self.token = token
        self.fields = info.fields + parametr
        self.sex = self.info['sex']
        b = datetime.datetime.now()
        dt = datetime.datetime.strptime(self.info['bdate'], '%d.%m.%Y')
        self.age = round((b - dt).days / 365)
        self.range = range
        self.list_people = []
        self.param_search = {'fields': self.fields,
                             'access_token': self.token,
                             'age_from': self.age - self.range,
                             'age_to': self.age + self.range,
                             'city': self.city_id,
                             'sort': 1,
                             'count': 1000,
                             'v': 5.103,
                             }
        if self.sex == 1:
            self.param_search['sex'] = 2
        elif self.sex == 2:
            self.param_search['sex'] = 1
        # Изменяет по желанию критерии для поиска
        print('''Желаете указать другие параметры для поиска? (да/нет)
                Иначе критериями для поиска будет информация о пользователе''')
        # выполняет запросы для получения id города для поиска
        flag = input('- ')
        if flag.lower() == 'да':
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
            if country_id in ['1', '2', '3']:
                print('Укажите город для поиска')
                city = input()
                param_id_city['country_id'] = country_id
                param_id_city['q'] = city
            response = requests.get('https://api.vk.com/method/database.getCities', params=param_id_city).json()
            self.param_search['city'] = response['response']['items'][0]['id']
            print('Укажите возраст кандидатов для поиска:')
            while True:
                try:
                    self.age = int(input('- '))
                    break
                except ValueError:
                    continue
            print('Укажите погрешность возраст для поиска:')
            while True:
                try:
                    self.range = int(input('- '))
                    break
                except ValueError:
                    continue

    def json_all_result_search(self):
        self.list_people.append(self.search_vk()['items'][0])
        with open(f'Cache\\{self.user_id}.json', 'w', encoding='utf-8') as file:
            json.dump(self.list_people, file, ensure_ascii=False, indent=2)

    def search_vk(self):
        peoples = requests.get('https://api.vk.com/method/users.search', params=self.param_search).json()['response']
        return peoples

    def friends_groups_user(self, users_id):
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
        for interests in self.info['interests']:
            interests_user.append(interests.lower().strip()) # получает список интересов пользователя из его данных
        for people in tqdm(self.search_vk()['items'], ncols=100): # Начисляет баллы совместимости
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
            if list_friends_people and list_friends_user: # сравнивает дрзуей человека и пользователя, за каждого друга +3 к совместимости
                for friend in list_friends_user:
                    if friend in list_friends_people:
                        count_compability += 3
            if list_groups_people and list_groups_user:# сравнивает группы человека и пользователя, за каждую группу +2 к совместимости
                for group in list_groups_user:
                    if group in list_groups_people:
                        count_compability += 2
            if 'bdate' in people.keys(): # Считает возраст человека и сравнивает его с возрастом пользователя
                if len(people['bdate']) > 5: # В зависимости от разницы начисляет баллы
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
            if 'interests' in people.keys(): # сравнивает интересы человека и пользователя
                if people['interests']:
                    interests_people = []
                    for interests in people['interests']:
                        interests_people.append(interests.lower().strip())
                    for interests in interests_user:
                        if interests in interests_people:
                            count_compability += 0.5
            value_compability[people['id']] = count_compability # Формирует словарь id - совместимость

        return value_compability


if __name__ in '__main__':
    user = Search()
    # pprint(user.search_vk())
    user.json_all_result_search()
