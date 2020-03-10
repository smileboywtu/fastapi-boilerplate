# -*- coding: utf-8 -*-


"""

postgre SQL database process driver


"""
import asyncio
from operator import attrgetter

import asyncpg


class PostgresDriver(object):
    __slots__ = ["conn", "sql_path", "query"]

    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            loop = asyncio.get_event_loop()
            cls.instance = loop.run_until_complete(
                cls.create_new_pg_instance(host=kwargs.get("host"), port=kwargs.get("port", 5432),
                                           user=kwargs.get("user", "postgres"), database=kwargs.get("database"),
                                           password=kwargs.get("password")))
        # make sure __init__ by invoked
        return super(PostgresDriver, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        """

        special params:
        - sql file path
        - record classes

        :param args:
        :param kwargs:
        """
        self.conn = self.instance
        self.sql_path = kwargs.get("sql_path")
        # self.query = aiosql.from_path(kwargs.get("sql_path"), "asyncpg", record_classes=kwargs.get("record_classes"))

    @classmethod
    async def destory(cls):
        """
        close connect pool

        :return:
        """
        if cls.instance:
            await cls.instance.close()
        cls.instance = None

    async def execute_sql(self, sql_name: str, *args, **kwargs):
        """
        execute sql with name

        :param sql_name:
        :return:
        """
        with self.conn.acquire() as connection:
            try:
                return await attrgetter(self.query)(sql_name)(connection, *args, **kwargs)
            except AttributeError:
                raise AttributeError("sql not defined in aiosql, check the sql path: {0}".format(self.sql_path))

    @classmethod
    async def create_new_pg_instance(cls, host, port, user, database, password):
        """
        create new pg instance pool

        :param args:
        :param kwargs:
        :return:
        """
        return await asyncpg.create_pool(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port)


pg_client = PostgresDriver(user="aaa", host=12, port=333, database=44, password=55)
