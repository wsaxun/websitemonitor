import os
import logging
from logging.handlers import RotatingFileHandler

from monitor.utils.config import get_log_config
from monitor.utils.env import get_root


def log_init(name=None):
    logger = logging.getLogger(name)
    project_path = get_root()
    log_path = os.path.join(project_path, 'log/collect.log')
    if not os.path.isfile(log_path):
        os.mknod(log_path)
    log_config = get_log_config()
    size = log_config.get('log').get('size')
    count = log_config.get('log').get('size')
    log = RotatingFileHandler(log_path, maxBytes=size, backupCount=count)
    formats = logging.Formatter(
        '[ %(asctime)s ] [ %(levelname)s ] [ %(threadName)s ] '
        '[ %(funcName)s ] %(message)s')
    log.setFormatter(formats)
    logger.addHandler(log)
    logger.setLevel(logging.INFO)
    return logger
