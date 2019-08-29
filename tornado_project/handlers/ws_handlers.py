from tornado_project.common_utilities.middleware.ws_middle_base import WSMiddle


class ExampleHandler(WSMiddle):
    # middleware_list = ['lib.middleware.pingmiddle.PingMiddleware']
    def msg_handle(self, message):
        print(message)