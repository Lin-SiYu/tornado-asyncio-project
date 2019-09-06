
from tornado_project.common_utilities.redis.redis_base import RedisHandler
from tornado_project.handlers import APIHandler


class RedisAPIHandler(APIHandler):
    async def get(self):
        # async 方法内实例化对象
        # re = await RedisHandler.init()
        # print(re)
        # 使用__init__方法实例化，非单例
        re = RedisHandler()
        # print(re)
        conn = self.settings['redis'].get_conn()
        val = await conn.set('xxx', 123)
        # get_val = await conn..get('xxx')
        self.write(self.success_json('ok', '200', val))
