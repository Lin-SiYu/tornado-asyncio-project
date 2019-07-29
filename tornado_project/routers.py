from tornado_project.handlers.mongo_handlers import MongoHandler
from tornado_project.handlers.myhttp import MyHttp

url_patterns = [
    (r"/test", MyHttp),
    (r'/mongo', MongoHandler)

]