# -*- coding: utf-8 -*-
from celery import Celery

import config

if config.REDIS_PASSWD:
    redis_url = "redis://:{0}@{1}:{2}/{3}".format(
        config.REDIS_PASSWD,
        config.REDIS_HOST,
        config.REDIS_PORT,
        config.REDIS_DB
    )
else:
    redis_url = "redis://{0}:{1}/{2}".format(
        config.REDIS_HOST,
        config.REDIS_PORT,
        config.REDIS_DB
    )

celery_app = Celery(
    broker=redis_url,
    backend=redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

celery_app.autodiscover_tasks([
    "tasks",
], force=True)

celery_app.conf.beat_schedule = {
    "parse_log": {
        "task": "parse_log",
        "schedule": 30
    }
}
