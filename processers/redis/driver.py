# -*- coding: utf-8 -*-


"""

redis driver

"""

from operator import attrgetter

import msgpack
from starlette.applications import Starlette
from redis import asyncio as aioredis

from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import (
    BusyLoadingError,
    ConnectionError,
    TimeoutError
)


class MSGPackSerializer(object):
    @staticmethod
    def encode(value) -> str:
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @staticmethod
    def decode(value: str):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")


def register_redis(
        app: Starlette,
        host: str,
        port: int,
        db: int,
        password: str
) -> None:
    @app.on_event("startup")
    async def init_redis() -> None:  # pylint: disable=W0612
        await RedisDriver.create_new_instance(host, port, db, password)

    @app.on_event("shutdown")
    async def close_redis() -> None:  # pylint: disable=W0612
        await RedisDriver.destroy()


class RedisDriver(object):
    __slots__ = ["conn"]

    instance = None

    # def __new__(cls, host, port, db, passwd):
    #     if not cls.instance:
    #         loop = asyncio.get_event_loop()
    #         cls.instance = loop.run_until_complete(cls.create_new_instance(host, port, db, passwd))
    #     return super(RedisDriver, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        self.conn = self.instance

    @classmethod
    async def destroy(cls):
        if cls.instance:
            await cls.instance.close()
        cls.instance = None

    @classmethod
    async def create_new_instance(cls, host, port, db, passwd, maxsize=512, timeout=3):
        """
        create new redis connection pool

        :return:
        """
        retry = Retry(ExponentialBackoff(), retries=3)
        cls.instance = await aioredis.Redis(
            host=host, port=port,
            db=db,
            password=passwd,
            socket_timeout=timeout,
            socket_connect_timeout=1,
            max_connections=maxsize,
            retry=retry,
            retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            retry_on_timeout=True,
            auto_close_connection_pool=True
        )

    def __getattr__(self, item):
        return attrgetter(item)(self.conn)

    @staticmethod
    def dumps(value):
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @staticmethod
    def loads(value):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")
