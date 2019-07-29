from tornado_project.handlers.myhttp import MyHttp

url_patterns = [
    (r"/test", MyHttp),
    # (r"/", TestWebSocketHandler),
    # (r"/quota", QuotaWebSocketHandler),

]