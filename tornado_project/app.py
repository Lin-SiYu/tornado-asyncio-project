from tornado.ioloop import IOLoop
from tornado.web import Application

from tornado_project.common_utilities.rabbit_mq.mq_base import MqBase
from tornado_project.common_utilities.redis.redis_base import RedisHandler
from tornado_project.common_utilities.sql.sql_base import MySQLHandler
from .routers import url_patterns
from .common_utilities.log.loggers import log_function

from .common_utilities.mongo.mongo_base import MongodbHandler


def make_app(cookie_secret, debug):
    mongo = MongodbHandler()
    sql = MySQLHandler()
    # redis = IOLoop.current().run_sync(RedisHandler.init)
    redis = RedisHandler()
    app = Application(
        handlers=url_patterns,
        cookie_secret=cookie_secret,
        log_function=log_function,
        debug=debug,
        mongo=mongo,
        sql=sql,
        redis=redis
    )
    app.mq = MqBase()
    return app
