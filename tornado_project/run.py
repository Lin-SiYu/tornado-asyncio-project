import os
import signal
import sys
import time

from tornado import httpserver
from tornado.ioloop import IOLoop
from tornado.options import options

from tornado_project.common_utilities.log import init_log, logger_info
from tornado_project.common_utilities.rabbit_mq.consumer import consumer
from tornado_project.config import parse_options
from tornado_project.mq_consumer_register import register


class Main:
    def __init__(self):
        self.loop = None
        self.app = None
        self.initialize()

    def initialize(self):
        # load settings
        self.set_working_dir()
        parse_options()

        # create app and update settings
        # ！！注意，为确保options等初始化操作做完，必须在该位置导入，否则options无法全局使用
        # 若先import后初始化，会编译路由，导致未初始化的option调用失败
        from tornado_project.app import make_app
        self.app = make_app(options.COOKIE_SECRET, options.DEBUG)
        init_log()

        self._get_loop()
        from tornado_project.common_utilities.heartbeat import heartbeat
        self.loop.call_later(0.5, heartbeat.ticker, app=self.app)
        self.loop.run_sync(self.app.mq.connect)
        self._init_subscribe()

    def start_server(self):
        http_server = httpserver.HTTPServer(self.app)
        http_server.listen(options.PORT)
        self.make_safely_shutdown(http_server, self.loop)
        logger_info.info('server start')
        self.loop.start()

    def _get_loop(self):
        if not self.loop:
            self.loop = IOLoop.instance()
        return self.loop

    def set_working_dir(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(project_dir)
        os.chdir(project_dir)

    def make_safely_shutdown(self, server, io_loop):
        def stop_handler(*args, **keywords):

            def shutdown():
                server.stop()
                # 根据业务调整该超时时间
                deadline = time.time() + options.SHUTDOWN_MAX_WAIT_TIME

                def stop_loop():
                    now = time.time()
                    if now < deadline:
                        io_loop.add_timeout(now + 1, stop_loop)
                    else:
                        io_loop.stop()

                stop_loop()

            io_loop.add_callback_from_signal(shutdown)

        # signal.signal(signal.SIGQUIT, stop_handler)
        signal.signal(signal.SIGTERM, stop_handler)
        signal.signal(signal.SIGINT, stop_handler)

    def _init_subscribe(self):
        '''
        MQ 消费者，初始化队列+监听
        :return:
        '''
        self.loop.run_sync(register)
        for data_dict in consumer.subscribers:
            self.loop.add_callback(self.app.mq.consumer, **data_dict)
            self.loop.add_callback(self.app.mq.subscribe, **data_dict)



if __name__ == '__main__':
    Main().start_server()
