import os
import signal
import sys
import time

from tornado import httpserver
from tornado.ioloop import IOLoop
from tornado.options import options

from tornado_project.app import make_app
from tornado_project.common_utilities.log import init_log,logger_info
from tornado_project.config import parse_options


def set_working_dir():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(project_dir)
    sys.path.append(project_dir)
    os.chdir(project_dir)


def make_safely_shutdown(server, io_loop):
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


def start_server():
    """
        启动服务
        :return:
        """
    # load settings
    set_working_dir()
    parse_options()
    # create app and update settings
    app = make_app(options.COOKIE_SECRET, options.DEBUG)
    init_log()

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.PORT)
    io_loop = IOLoop.instance()
    make_safely_shutdown(http_server, io_loop)
    logger_info.info('server start')
    io_loop.start()


if __name__ == '__main__':
    start_server()
