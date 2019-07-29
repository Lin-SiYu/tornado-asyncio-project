from tornado import gen

from ..handlers import APIHandler


class MyHttp(APIHandler):
    @gen.coroutine
    def get(self):
        res = yield self.gen_test()
        self.write(res)
        # raise HTTPAPIError(10011)

    @gen.coroutine
    def gen_test(self):
        raise gen.Return(self.success_json('1', '2', '3'))