# -*- coding: utf-8 -*-

"""

for development just run: python run.py
for production run docker file with make tool

"""

import uvicorn
from handlers.application import app_instance

# run the web api server by using uvicorn
# just for development
# uvicorn.run(app_instance)

# for production run use docker file
# use Gunicorn with uvicorn loop class
# see docker file
