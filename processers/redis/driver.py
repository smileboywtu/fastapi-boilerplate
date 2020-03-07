# -*- coding: utf-8 -*-


"""

redis driver

"""

import asyncio
from operator import attrgetter

import aioredis
import msgpack


class MSGPackSerializer(object):
    @staticmethod
    def encode(value) -> str:
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @staticmethod
    def decode(value: str):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")


class RedisDriver(object):
    __slots__ = ["conn"]

    instance = None

    def __new__(cls, host, port, db, passwd):
        if not cls.instance:
            loop = asyncio.get_event_loop()
            cls.instance = loop.run_until_complete(cls.create_new_instance(host, port, db, passwd))
        return super(RedisDriver, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        self.conn = self.instance

    @classmethod
    async def create_new_instance(cls, host, port, db, passwd, maxsize=512, minsize=256, timeout=3):
        """
        create new redis connection pool

        :return:
        """
        return await aioredis.create_redis_pool(
            address=[host, port],
            db=db,
            password=passwd,
            minsize=minsize,
            maxsize=maxsize,
        )

    def __getattr__(self, item):
        return attrgetter(self.conn)

    @staticmethod
    def dumps(value):
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @staticmethod
    def loads(value):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")
