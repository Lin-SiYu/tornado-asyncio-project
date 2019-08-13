import asyncio

import aioredis
from tornado.options import options


class RedisHandler:
    def __init__(self):
        # 非单例，开启loop后需等待执行完毕才可进行API调用操作
        asyncio.get_event_loop().create_task(self.connection())

    @classmethod
    async def connection(cls):
        option_data = options.as_dict()
        db_dict = dict(
            db=option_data.get('REDIS_DB', None),
            password=option_data.get('REDIS_PWD', None),
            minsize=option_data.get('REDIS_MIN', 5),
            maxsize=option_data.get('REDIS_MAX', 10),
        )
        conn = await aioredis.create_redis_pool(
            option_data.get('REDIS_URL'), encoding='utf8',
            **db_dict
        )
        cls.conn = conn
        return conn

    # @classmethod
    # async def init(cls):
    #     if not hasattr(cls, "_instance"):
    #         cls.conn = await cls.connection()
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    def get_conn(self):
        return self.conn
