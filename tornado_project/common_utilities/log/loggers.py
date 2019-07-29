import datetime
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

from tornado.log import access_log
from tornado.options import options


def log_function(handler):
    """
    log function to log access request information

    regex parse: (?<remote_ip>[\d.]+) [-\w]+ [-\w]+ \[(?<request_date>[\d\/:\s\+]+)\] \"
    (?<http_method>[A-Z]+) (?<http_uri>[\/a-zA-Z\.]+) (?<http_version>[A-Z\/\d\.]+)\"
    (?<status_code>[\d]+) (?<length>[\d]+)
    (?<request_time>[\d\.]+) (?<request_id>[\d\w]+) [\w\-]+ \[(?<request_body>.+)\] -

    :param handler:
    :return:
    """

    _log_meta = dict(
        app_id="app-up",
        user="-",
        username="-",
        response_code="-",

        http_uri=handler.request.uri,
        http_status=handler.get_status(),
        http_method=handler.request.method,
        http_version=handler.request.version,

        remote_ip=handler.request.remote_ip,
        request_time=1000.0 * handler.request.request_time(),

        response_length=handler.request.headers.get("Content-Length", 0),
        request_args=handler.request.arguments,
        request_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    request_time = _log_meta['request_time']
    if float(request_time) > 1000:
        _log_meta['request_time'] = str(round(float(request_time) / 1000, 2)) + 's'
    else:
        _log_meta['request_time'] = str(round(float(request_time), 2)) + 'ms'

    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error

    log_method("[%(request_date)s] %(remote_ip)s %(user)s %(username)s - \"%"
               "(http_method)s %(http_uri)s %(http_version)s\" %(http_status)s - "
               "%(response_length)sbyte - %(request_time)s - %(app_id)s - [%(request_args)s] -", _log_meta)


def logger_config(name, path, level, log_format, rotate_interval, backup_count,
                  debug=False):
    """
     配置 log app 对象

    :param name: 日志名称
    :param path: 日志文件路径
    :param level: 日志等级
    :param log_format: 日志格式
    :param max_bytes: 日志文件最大大小
    :param backup_count: 日志文件滚动个数
    :param debug: True 使用控制台输出, 默认 False
    :return:
    """
    logger = logging.getLogger(name)
    handler = TimedRotatingFileHandler(
        path, when='D', interval=rotate_interval, backupCount=backup_count,
        encoding="utf-8") \
        if not debug else \
        logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    log_level = getattr(logging, level)
    logger.setLevel(log_level)
    logger.addHandler(handler)


def configure_tornado_logger(path, interval, backup_count,
                             level,
                             name="tornado.application",
                             debug=False):
    """

    ## read doc:
    https://docs.python.org/3/library/logging.html#logrecord-attributes

    tornado web application log_format:
    %(asctime)s %(levelname)s %(request_id)-%(process)d %(filename)s:%(lineno)d -- %(message)s

    :param path: log file path
    :param level: log level
    :param name: log name
    :param debug: if debug, show logs on stdout
    :return:
    """
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    if name == "tornado.access":
        log_format = "[%(name)s] %(message)s"
    elif name == "plugins":
        log_format = "[%(name)s] %(asctime)s %(levelname)s -- %(message)s"
    else:
        log_format = "[%(name)s] %(asctime)s %(levelname)s %(filename)s:%(lineno)d -- %(message)s"

    return logger_config(
        name=name,
        path=path,
        level=level,
        log_format=log_format,
        # max_bytes=100 * 1024 * 1024,
        rotate_interval=interval,
        backup_count=backup_count,
        debug=debug
    )
