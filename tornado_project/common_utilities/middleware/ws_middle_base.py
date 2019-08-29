import importlib
import json

from tornado.options import options
from tornado.websocket import WebSocketHandler

from tornado_project.common_utilities.log import logger_info
from ..middleware import WS_CONNECT_USER_INFOS as user_infos


class WSMiddleware:
    '''
    process_open、process_message、process_close
    三者参数，self = ws = <app.handlers.ws_handlers.MarketPairHandler object at 0x000001F16AE0DCF8>
    '''

    def process_open(self, ws):
        pass

    def process_message(self, ws):
        pass

    def process_close(self, ws):
        pass


class WSMiddle(WebSocketHandler):
    def open(self):
        logger_info.info('%s - WSMiddle opened success!' % self)
        try:
            self.middleware_list
        except AttributeError:
            self.middleware_list = options.MIDDLEWARE_LIST

        # 初始化放置用户信息的字典，添加对应的类
        for middleware in self.middleware_list:
            mpath, mclass = middleware.rsplit('.', maxsplit=1)
            if not mclass in user_infos:
                user_infos[mclass] = {}

        self._middle_list_handle('process_open')

    def on_message(self, message):
        # print("WSMiddle on_message")
        self.message = message
        self._middle_list_handle('process_message')
        self.msg_handle(message)

    def msg_handle(self, message):
        pass

    def on_close(self):
        # print("WSMiddle closed")
        logger_info.info('%s - WSMiddle closed !' % self)
        self._middle_list_handle('process_close')

    def _middle_list_handle(self, process_func_name):
        for middleware in self.middleware_list:
            mpath, mclass = middleware.rsplit('.', maxsplit=1)
            mod = importlib.import_module(mpath)
            # getattr(mod, mclass).process_open(self, self)
            cla_obj = getattr(mod, mclass)
            func = getattr(cla_obj, process_func_name)
            func(self, self)

    # 允许所有跨域通讯，解决403问题
    def check_origin(self, origin):
        return True

    def success_json(self, data, msg='ok'):
        res = dict(
            status='200',
            msg=msg,
            data=data
        )
        return json.dumps(res)
