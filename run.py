# -*- coding: utf-8 -*-

"""

for development just run: python run.py
for production run docker file with make tool

"""

import uvicorn

# run the web api server by using uvicorn
# just for development
# load app after env set
from handlers.application import app_instance

# for test
# uvicorn.run(app_instance)

# for production run use docker file
# use Gunicorn with uvicorn loop class
# see docker file
