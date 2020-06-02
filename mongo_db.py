from pymongo import MongoClient


class Mongo_DB():

    def __init__(self, database):
        self.db = database
        self.data = []

    def create_db(self):
        '''Создаёт подключение к БД, саму БД'''
        self.client = MongoClient()
        self.mongo_db = self.client[self.db]

    def create_coll(self, table):
        '''Создаёт коллекцию'''
        self.events = self.mongo_db[table]

    def input_data_many(self, data):
        '''Записывает данные в БД'''
        res_id = self.events.insert_many(data).inserted_ids
        return res_id

    def input_data(self, data):
        """Записывает один объект в БД"""
        res_id = self.events.insert_one(data).inserted_id
        return res_id

    def read(self):
        '''Читает данные из БД и записывает их в параметр data класса'''
        for i in self.events.find():
            self.data.append(i)

    def del_doc_coll(self):
        '''Очищает коллекцию'''
        self.events.remove({})

    def show_coll(self):
        """Отображает коллеции в БД"""
        return self.mongo_db.collection_names()

    def del_coll(self):
        """Удаляет коллекцию"""
        self.events.drop()


if __name__ in '__main__':
    pass
