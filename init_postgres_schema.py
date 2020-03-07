# -*- coding: utf-8 -*-


"""

init all the table inside postgres

"""

import asyncio

from processers.postgres_process import init_postgres_schema

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



