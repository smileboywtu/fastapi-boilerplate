# -*- coding: utf-8 -*-

"""


web application config file


"""

import os


# project root directory
BASE_DIR = os.path.join(os.pardir, os.path.dirname(__file__))

# sql query directory
SQL_PATH = os.path.join(BASE_DIR, "sql_query", "sql")


# postgres database config


# notice: change docker file if you want to change
# this port number
WEB_APP_PORT_NUMBER = 8000

# log file path
