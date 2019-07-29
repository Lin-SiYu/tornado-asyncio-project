from tornado import gen

from tornado_project.handlers import APIHandler


class MongoHandler(APIHandler):
    @gen.coroutine
    def get(self):
        mongo = self.settings['mongo']
        res = yield mongo.do_find_one('testtable', {'name': 'name'})
        print(res)
        r = yield  mongo.do_find('testtable',limit=3)
        print(r)
        self.write('ok')

