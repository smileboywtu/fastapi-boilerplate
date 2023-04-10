# -*- coding: utf-8 -*-

"""


web application config file


"""

import os

# project root directory
BASE_DIR = os.path.join(os.pardir, os.path.dirname(__file__))

# sql query directory
SQL_PATH = os.path.join(BASE_DIR, "sql_query", "sql")

# notice: change docker file if you want to change
# this port number
# --------------------------------------------------------------------
WEB_APP_PORT_NUMBER = 8000

# log file path
# --------------------------------------------------------------------
enable_access_log = True
log_socket_host = os.environ.get("TCP_SERVER_LOG_HOST", "")
log_socket_port = int(os.environ.get("TCP_SERVER_LOG_PORT", 7779))

# redis config
# --------------------------------------------------------------------
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")  # docker network
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
REDIS_PASSWD = os.environ.get("REDIS_PASSWD", "")

# postgres database config
# --------------------------------------------------------------------
# notice use docker with service name
PG_HOST = os.environ.get("POSTGERS_HOST", "postgres")
PG_PORT = os.environ.get("POSTGERS_PORT", 5432)
PG_DATABASE = os.environ.get("POSTGRES_DB", "fast")
PG_PASSWD = os.environ.get("POSTGRES_PASSWORD", "")
PG_USER = os.environ.get("POSTGRES_USER", "fast_user")

# config log
# --------------------------------------------------------------------
LOG_BASE_DIR = '/logs'
access_log_path = os.path.join(LOG_BASE_DIR,'access.log')
access_logger_name = "fastapi.access"
access_socker_logger_name = "fastapi.access.socket"