# -*- coding: utf-8 -*-

"""

create web application and use in different
handlers

"""

import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from pydantic import ValidationError
from starlette.applications import Starlette

import config
from handlers.middlware import RequestIDMiddleware, AccessLogMiddleware
from handlers.tools import GeneralJSONResponse
from processers.postgres.driver import register_postgres
from processers.redis.driver import register_redis
from tasks.health import check_redis, check_postgres
from utils.logs import config_socket_logger, access_log_format
from .users.handler import user_router

# config logger
access_logger_name = "fastapi.access"
access_logger = config_socket_logger(access_logger_name, access_log_format, "INFO",
                                     socket_host=config.log_socket_host,
                                     socket_port=config.log_socket_port)


def register_health(
        app: Starlette
) -> None:
    @app.on_event("startup")
    async def init_check() -> None:  # pylint: disable=W0612
        code, msg = await check_redis(config.REDIS_HOST, config.REDIS_PORT)
        assert code == 0, msg
        code, msg = await check_postgres(config.PG_HOST, config.PG_PORT)
        assert code == 0, msg


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
app_instance = FastAPI(exception_handlers=exception_handlers)

# init postgres connection
register_health(app=app_instance)
register_postgres(app=app_instance, user=config.PG_USER, host=config.PG_HOST, port=config.PG_PORT,
                  db=config.PG_DATABASE, password=config.PG_PASSWD)
register_redis(app=app_instance, host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB,
               password=config.REDIS_PASSWD)

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
app_instance.include_router(prefix="/api/v1/user",
                            router=user_router, tags=["user"])
