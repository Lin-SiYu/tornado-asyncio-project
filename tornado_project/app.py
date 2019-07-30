from tornado.web import Application

from tornado_project.common_utilities.sql.sql_base import MySQLHandler
from .routers import url_patterns
from .common_utilities.log.loggers import log_function

from .common_utilities.mongo.mongo_base import MongodbHandler


def make_app(cookie_secret, debug):
    mongo = MongodbHandler()
    sql = MySQLHandler()

    app = Application(
        handlers=url_patterns,
        cookie_secret=cookie_secret,
        log_function=log_function,
        debug=debug,
        mongo=mongo,
        sql=sql,
    )
    return app
