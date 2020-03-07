# -*- coding: utf-8 -*-


"""

function related to redis

"""

from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWD
from .redis.driver import RedisDriver

# create redis client
redis_client = RedisDriver(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWD)

# -------------------- function helper space ------------------------------
