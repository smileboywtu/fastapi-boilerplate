# -*- coding: utf-8 -*-


"""

redis driver

"""

from operator import attrgetter

import aioredis
import msgpack
from starlette.applications import Starlette


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
            cls.instance.close()
            await cls.instance.wait_closed()
        cls.instance = None

    @classmethod
    async def create_new_instance(cls, host, port, db, passwd, maxsize=512, minsize=256, timeout=3):
        """
        create new redis connection pool

        :return:
        """
        cls.instance = await aioredis.create_redis_pool(
            address=[host, port],
            db=db,
            password=passwd,
            minsize=minsize,
            maxsize=maxsize,
        )

    def __getattr__(self, item):
        return attrgetter(self.conn)(item)

    @staticmethod
    def dumps(value):
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @staticmethod
    def loads(value):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")
