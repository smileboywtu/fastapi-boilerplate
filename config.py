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

# redis config
# --------------------------------------------------------------------
REDIS_HOST = "10.80.186.87"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWD = "geetest456"

# postgres database config
# --------------------------------------------------------------------
PG_HOST = "127.0.0.1"
PG_PORT = 5432
PG_DATABASE = "gcloud"
PG_PASSWD = "geetest"
PG_USER = "psql_demo"
