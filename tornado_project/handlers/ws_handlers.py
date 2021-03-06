from tornado_project.common_utilities.ws_base import WSHandler


class ExampleHandler(WSHandler):
    # 局部列表是在全局列表的叠加而不是覆盖
    # middleware_list = ['lib.middleware.pingmiddle.PingMiddleware']
    def open_handle(self):
        # 在middleware执行后执行该方法，链接打开时调用
        pass

    def msg_handle(self, message):
        print(message)

    def close_handle(self):
        # 在middleware执行后执行该方法，连接关闭时调用
        pass

    # with async using
    # async def open_handle(self):
    #     pass
    # async def msg_handle(self, message):
    #     print(message)