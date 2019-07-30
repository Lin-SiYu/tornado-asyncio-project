import peewee_async
from tornado.options import options

from tornado_project.common_utilities.log import logger_error


class MySQLHandler:
    def __init__(self):
        try:
            db_dic = dict(
                host=options['SQL_HOST'],
                port=options['SQL_POST'],
                user=options['SQL_USER'],
                password=options['SQL_PWD'],
                max_connections=options['SQL_MAX_CONN'],
                database=options['SQL_DB_NAME'],
            )
            self.conn = peewee_async.PooledMySQLDatabase(**db_dic, charset='utf8mb4')
            self.manager = peewee_async.Manager(self.conn)
        except AttributeError as e:
            logger_error.error('AttributeError:%s' % e)

    def get_manager(self):
        return self.manager

    def get_conn(self):
        return self.conn
