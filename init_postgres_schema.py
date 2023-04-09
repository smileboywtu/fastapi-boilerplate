# -*- coding: utf-8 -*-


"""

init all the table inside postgres

"""
import asyncio

from handlers.users import models as user_model
from processers.postgres_process import init_postgres_schema, pg_client


def init_postgres_other_model():
    print("WARNING: are you sure to init postgres database?")
    print("**please make sure you just run once ")
    while True:
        readline = input("press Y/N , default N")
        if readline == "N":
            print("exit to init postgres schema")
            break
        elif readline == "Y":
            print("start to init postgres schema")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(init_postgres_schema())
            print("postgres schema inited")
            break
        else:
            print("enter Y/N?")


async def init_postgres_orm_model():
    # init db schema
    async with pg_client.alchemy_engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.create_all)

    print("init orm done")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_postgres_orm_model())
