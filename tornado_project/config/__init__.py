import logging
import os

from tornado.options import options, define, parse_command_line


def parse_config_file(path):
    """Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.

    This version allow customize new options which are not defined before
    from a configuration file.
    """
    config = {}
    exec(compile(open(path, "rb").read(), path, 'exec'), config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


def parse_options():
    _root = os.getcwd()
    _settings = os.path.join(_root, "config", "configs.py")
    print(_settings)
    try:
        parse_config_file(_settings)
        logging.info("Using settings.py as default settings.")
    except Exception as e:
        logging.error("No any default settings, are you sure? Exception: %s" % e)
        raise e

    parse_command_line()
