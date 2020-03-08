# -*- coding: utf-8 -*-


"""

init all the table inside postgres

"""

import asyncio

import tortoise

from config import PG_DATABASE_URL
from handlers.users import models as user_model
from processers.postgres_process import init_postgres_schema


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


def init_postgres_orm_model():
    # init database
    await tortoise.Tortoise.init(db_url=PG_DATABASE_URL, modules={"models": [user_model.__name__]})

    # init db schema
    tortoise.generate_schema_for_client()

    print("init orm done")


if __name__ == '__main__':
    init_postgres_orm_model()