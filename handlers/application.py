# -*- coding: utf-8 -*-

"""

create web application and use in different
handlers

"""

import traceback
from functools import partial

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from pydantic import ValidationError
from tortoise.contrib.starlette import register_tortoise

import config
from handlers.middlware import RequestIDMiddleware, AccessLogMiddleware
from handlers.tools import GeneralJSONResponse
from processers.postgres.driver import PostgresDriver
from processers.redis.driver import RedisDriver
from tasks.health import check_redis, check_postgres
from utils.logs import config_socket_logger, access_log_format
from .users.handler import user_router

# start up task
check_redis_func = partial(check_redis, config.REDIS_HOST, config.REDIS_PORT)
check_postgres_func = partial(check_postgres, config.PG_HOST, config.PG_PORT)

# config logger
access_logger_name = "fastapi.access"
access_logger = config_socket_logger(access_logger_name, access_log_format, "INFO",
                                     socket_host=config.log_socket_host,
                                     socket_port=config.log_socket_port)


# general exception
def handle_general_exception(request: Request, exc: HTTPException):
    # HTTPException is an based on Exception
    # for general debug , or batter you can write this to log file
    # print(exc.detail)
    print(traceback.print_exc())
    return GeneralJSONResponse(code=4000, data={}, detail=str(exc))


# handler params exception
def handler_params_exception(request: Request, exc: HTTPException):
    # print(exc.detail)
    print(traceback.print_exc())
    return GeneralJSONResponse(code=3000, data={}, detail=str(exc))


exception_handlers = {
    Exception: handle_general_exception,
    ValidationError: handler_params_exception
}

# define application
app_instance = FastAPI(
    on_startup=[
        check_redis_func,
        check_postgres_func
    ],
    on_shutdown=[
        RedisDriver.destroy,
        PostgresDriver.destory
    ],
    exception_handlers=exception_handlers
)

# init postgres connection
register_tortoise(app=app_instance, db_url=config.PG_DATABASE_URL, modules={"models": ["handlers.users.models"]})

# add middleware
# middleware execute from top down, first add execute firstly
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app_instance.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app_instance.add_middleware(
    RequestIDMiddleware,
    mode="uuid"
)

# make this below request id middleware
if config.enable_access_log:
    app_instance.add_middleware(
        AccessLogMiddleware,
        log_name=access_logger_name
    )

# add user router
app_instance.include_router(prefix="/api/v1/user", router=user_router, tags=["user"])
