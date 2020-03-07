# -*- coding: utf-8 -*-


"""

function related to postgres

"""

from config import PG_HOST, PG_PORT, PG_DATABASE, PG_PASSWD, PG_USER
from .postgres.driver import PostgresDriver

# create redis client
pg_client = PostgresDriver(user=PG_USER, host=PG_HOST, port=PG_PORT, database=PG_DATABASE, password=PG_PASSWD)


# -------------------- function helper space ------------------------------
async def init_postgres_schema():
    """
    this function only need to execute once, you'd batter to do this with init_schema.py
    :return:
    """
    await pg_client.execute_sql("init_postgres_schema")


