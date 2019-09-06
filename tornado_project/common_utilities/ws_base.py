import importlib

from tornado.options import options
from tornado.websocket import WebSocketHandler

from tornado_project.common_utilities.middleware import WS_CONNECT_USER_INFOS as user_infos
from tornado_project.common_utilities.tools import get_gzip


class WSResponseHandler(object):

    @staticmethod
    def return_result(message, code, data):
        result = {
            "code": code,
            "msg": message,
            "data": data
        }

        return get_gzip(result)

    @staticmethod
    def success_result(data):
        result = {
            "code": 200,
            "msg": 'ok',
            "data": data
        }
        return get_gzip(result)


class WSMiddleware(WSResponseHandler):
    '''
    process_open、process_message、process_close
    三者参数，ws = <app.handlers.ws_handlers.MarketPairHandler object at 0x000001F16AE0DCF8>
    '''

    def process_open(self, ws):
        pass

    def process_message(self, ws):
        pass

    def process_close(self, ws):
        pass


class WSHandler(WebSocketHandler, WSResponseHandler):
    _open_middleware = []
    _message_middleware = []
    _close_middleware = []

    def open(self):
        self._middle_list_handle()
        for open_func in self._open_middleware:
            open_func(self)
        self.open_handle()

    def open_handle(self):
        pass

    def on_message(self, message):
        self.message = message
        for msg_func in self._message_middleware:
            msg_func(self)
        self.msg_handle(message)

    def msg_handle(self, message):
        pass

    def on_close(self):
        for close_func in self._close_middleware:
            close_func(self)
        self.close_handle()

    def close_handle(self):
        pass

    def _middle_list_handle(self):
        try:
            self.middleware_list = list(set(options.MIDDLEWARE_LIST) | set(self.middleware_list))
        except AttributeError:
            self.middleware_list = options.MIDDLEWARE_LIST

        for middleware in self.middleware_list:
            try:
                mpath, mclass = middleware.rsplit('.', maxsplit=1)
            except ValueError as err:
                raise ImportError("%s doesn't look like a module path" % middleware) from err

            # 初始化放置用户信息的字典，添加对应的类
            if not mclass in user_infos:
                user_infos[mclass] = {}

            mod = importlib.import_module(mpath)
            try:
                cla_obj = getattr(mod, mclass)
                mw_instance = cla_obj()
                if hasattr(mw_instance, 'process_open'):
                    self._open_middleware.append(mw_instance.process_open)
                if hasattr(mw_instance, 'process_message'):
                    self._message_middleware.append(mw_instance.process_message)
                if hasattr(mw_instance, 'process_close'):
                    self._close_middleware.append(mw_instance.process_close)
            except AttributeError as err:
                raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
                    mpath, mclass)
                                  ) from err

    # 允许所有跨域通讯，解决403问题
    def check_origin(self, origin):
        return True
