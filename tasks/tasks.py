# -*- coding: utf-8 -*-

from .celery_app import celery_app


@celery_app.task(name="parse_log", ignore_result=True)
def parse_logs():
    print("parse_logs starting...")
