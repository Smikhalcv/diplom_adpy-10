from User.get_token import Token
from User.user_id import id_user
from search_peoples import Search
from mongo_db import Mongo_DB
from executor import get_result

if __name__ in '__main__':
    token = Token()
    token = token.read_token()
    user_id = str(id_user(token))
    database = Mongo_DB('VKinder')
    database.create_db()
    if user_id in database.show_coll():
        print('По данному пользователю уже проводился поиск, начать новый? (да/нет)')
        print('(при выборе нет, продолжит чтение из старого поиска)')
        flag = input('- ')
        if flag.lower().startswith('д'):
            user = Search(token, user_id)
            value_compability = user.compability()
            get_result(token, user_id)
        else:
            get_result(token, user_id)
    if user_id not in database.show_coll():
        user = Search(token, user_id)
        value_compability = user.compability()
        get_result(token, user_id)
