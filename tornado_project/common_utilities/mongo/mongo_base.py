import motor
from tornado.options import options


class MongodbHandler(object):
    def __init__(self, uri=None, db=None):
        try:
            if not uri:
                uri = options['MONGO_URI']
            self.client = motor.motor_tornado.MotorClient(uri)
            if not db:
                db = options['MONGO_DB']
            self.db = self.client[db]
        except AttributeError as e:
            print('AttributeError:', e)

    async def do_find_one(self, doc_name, filter=None, *args, **kwargs):
        return await self.db[doc_name].find_one(filter, *args, **kwargs)

    async def do_find(self, doc_name, filter=None, *args, **kwargs):
        cursor = self.db[doc_name].find(filter, *args, **kwargs)
        doc_list = []
        async for document in cursor:
            doc_list.append(document)
        return doc_list
