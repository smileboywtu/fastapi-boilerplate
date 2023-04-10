# -*- coding: utf-8 -*-

"""

logger handler for fastapi

usually we need logger:

- application access log
- app context log
- app general data log
- app monitor log

"""

import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

# access log formatter
access_log_format = "%(asctime)s %(levelname)s %(request_id)s %(time_cost).2f " \
                    "%(request_method)s %(request_path)s %(response_code)s"

log_format = "[%(name)s] %(asctime)s %(levelname)s %(request_id)s %(filename)s:%(lineno)d -- %(message)s"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


def logger_config(name, path, level, log_format, rotate_interval, backup_count,
                  debug=False):
    """
     配置 log handler 对象

    :param name: 日志名称
    :param path: 日志文件路径
    :param level: 日志等级
    :param log_format: 日志格式
    :param max_bytes: 日志文件最大大小
    :param backup_count: 日志文件滚动个数
    :return:
    """
    logger = logging.getLogger(name)

    handler = TimedRotatingFileHandler(
        path, when='D', interval=rotate_interval, backupCount=backup_count,
        encoding="utf-8") \
        if not debug else \
        logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(log_format)
    handler.setFormatter(formatter)
    log_level = getattr(logging, level)
    logger.setLevel(log_level)
    logger.addHandler(handler)


def config_socket_logger(logger_name, log_format, log_level, socket_host="127.0.0.1", socket_port=514):
    """
    config socket logger

    :param logger_name:
    :param log_format:
    :param log_level:
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    handler = logging.handlers.SocketHandler(
        host=socket_host, port=socket_port)
    handler.setFormatter(log_format)
    logger.addHandler(handler)