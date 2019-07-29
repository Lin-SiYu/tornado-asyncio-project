import logging
from tornado.options import options
from .loggers import configure_tornado_logger


def init_log():
    # 初始化 web 记录日志
    configure_tornado_logger(options.INFO_LOG_PATH,
                             options.LOG_ROTATE_DAY,
                             options.LOG_BACKUP,
                             'INFO',
                             name="app.info", debug=options.DEBUG)
    configure_tornado_logger(options.DEBUG_LOG_PATH,
                             options.LOG_ROTATE_DAY,
                             options.LOG_BACKUP,
                             'DEBUG',
                             name="app.debug",
                             debug=options.DEBUG)
    configure_tornado_logger(options.ERROR_LOG_PATH,
                             options.LOG_ROTATE_DAY,
                             options.LOG_BACKUP,
                             'ERROR',
                             name="app.error",
                             debug=options.DEBUG)
    configure_tornado_logger(options.ACC_LOG_PATH,
                             options.LOG_ROTATE_DAY,
                             options.LOG_BACKUP,
                             'INFO',
                             name="tornado.access",
                             debug=options.DEBUG)


logger_info = logging.getLogger('app.info')
logger_debug = logging.getLogger('app.debug')
logger_error = logging.getLogger('app.error')
