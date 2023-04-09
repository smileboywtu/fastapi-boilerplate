# -*- coding: utf-8 -*-


"""

function related to postgres

"""

from config import PG_HOST, PG_PORT, PG_DATABASE, PG_PASSWD, PG_USER, SQL_PATH
from .postgres.driver import PostgresDriver

# create redis client
pg_client = PostgresDriver(user=PG_USER, host=PG_HOST, port=PG_PORT,
                           database=PG_DATABASE, password=PG_PASSWD, sql_path=SQL_PATH)


# -------------------- function helper space ------------------------------
async def init_postgres_schema():
    """
    this function only need to execute once, you'd batter to do this with init_schema.py
    :return:
    """
    await pg_client.execute_sql("init_postgres_schema")


async def create_new_user(username, age, mobile, address):
    return await pg_client.execute_sql("add_new_user", username, age, mobile, address)


async def get_user_detail(): pass
