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
enable_access_log = False
log_socket_host = "127.0.0.1"
log_socket_port = 514

# redis config
# --------------------------------------------------------------------
REDIS_HOST = "redis"  # docker network
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWD = None

# postgres database config
# --------------------------------------------------------------------
PG_HOST = "postgres"  # notice use docker with service name
PG_PORT = 5432
PG_DATABASE = os.environ.get("POSTGRES_DB", "false")
PG_PASSWD = os.environ.get("POSTGRES_PASSWORD", "")
PG_USER = os.environ.get("POSTGRES_USER", "fast")
PG_DATABASE_URL = "postgres://{user}:{passwd}@{host}:{port}/{db}".format(user=PG_USER, passwd=PG_PASSWD, host=PG_HOST,
                                                                           port=PG_PORT, db=PG_DATABASE)
