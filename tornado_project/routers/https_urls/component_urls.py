from tornado_project.handlers.mongo_handlers import MongoHandler
from tornado_project.handlers.myhttp import MyHttp
from tornado_project.handlers.redis_handlers import RedisAPIHandler
from tornado_project.handlers.sql_handlers import SqlHandler

url_patterns = [
    (r"/test", MyHttp),
    (r'/mongo', MongoHandler),
    (r'/sql', SqlHandler),
    (r'/redis', RedisAPIHandler),
]