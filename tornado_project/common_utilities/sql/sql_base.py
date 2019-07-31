import peewee_async
from tornado.options import options


class MySQLHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            db_dic = dict(
                host=options['SQL_HOST'],
                port=options['SQL_POST'],
                user=options['SQL_USER'],
                password=options['SQL_PWD'],
                max_connections=options['SQL_MAX_CONN'],
                database=options['SQL_DB_NAME'],
            )
            cls.conn = peewee_async.PooledMySQLDatabase(**db_dic, charset='utf8mb4')
            cls.manager = peewee_async.Manager(cls.conn)
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_manager(self):
        return self.manager

    def get_conn(self):
        return self.conn
