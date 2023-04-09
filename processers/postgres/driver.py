# -*- coding: utf-8 -*-


"""

postgre SQL database process driver


"""
from operator import attrgetter

import aiosql
import asyncpg
import asyncio
from starlette.applications import Starlette
from sqlalchemy.ext.asyncio import create_async_engine


def register_postgres(
        app: Starlette,
        host: str,
        port: int,
        db: int,
        user: str,
        password: str
) -> None:
    @app.on_event("startup")
    async def init_postgres() -> None:  # pylint: disable=W0612
        await PostgresDriver.create_new_pg_instance(host, port, user, db, password)

    @app.on_event("shutdown")
    async def close_postgres() -> None:  # pylint: disable=W0612
        await PostgresDriver.destory()


class PostgresDriver(object):
    __slots__ = ["conn", "sql_path", "query"]

    instance = None
    alchemy_engine = None

    def __init__(self, *args, **kwargs):
        """

        special params:
        - sql file path
        - record classes

        :param args:
        :param kwargs:
        """
        if not self.instance:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                PostgresDriver.create_new_pg_instance(**kwargs))
        self.conn = self.instance
        self.sql_path = kwargs.get("sql_path")
        self.query = aiosql.from_path(kwargs.get(
            "sql_path"), "asyncpg", record_classes=kwargs.get("record_classes"))

    @classmethod
    async def destory(cls):
        """
        close connect pool

        :return:
        """
        if cls.instance:
            await cls.instance.close()
        if cls.alchemy_engine:
            await cls.alchemy_engine.dispose()
        cls.instance = None
        cls.alchemy_engine = None

    async def execute_sql(self, sql_name: str, *args, **kwargs):
        """
        execute sql with name

        :param sql_name:
        :return:
        """
        conn = await self.conn.acquire()
        try:
            return await attrgetter(sql_name)(self.query)(conn, *args, **kwargs)
        except AttributeError:
            raise AttributeError(
                "sql not defined in aiosql, check the sql path: {0}".format(self.sql_path))
        finally:
            await self.conn.release(conn)

    @classmethod
    async def create_new_pg_instance(cls, host, port, user, database, password, **kwages):
        """
        create new pg instance pool

        :param args:
        :param kwargs:
        :return:
        """
        cls.instance = await asyncpg.create_pool(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port)
        cls.alchemy_engine = create_async_engine("postgresql+asyncpg://{user}:{passwd}@{host}:{port}/{db}".format(
            host=host, port=port, user=user, passwd=password, db=database))
