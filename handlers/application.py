# -*- coding: utf-8 -*-

"""

create web application and use in different
handlers

"""

from fastapi import FastAPI

from .users.handler import user_router

# define application

app_instance = FastAPI()

# add user router
app_instance.add_route(name="users", path="/api/v1/user", route=user_router)
