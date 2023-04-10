# -*- coding: utf-8 -*-


"""

application middleware

example middleware

"""
import logging
import resource
import time

from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from handlers.tools import generate_request_id_by_uuid


# from https://github.com/steinnes/timing-asgi/blob/master/timing_asgi/utils.py
def get_cpu_time():
    resources = resource.getrusage(resource.RUSAGE_SELF)
    # add up user time (ru_utime) and system time (ru_stime)
    return resources[0] + resources[1]


class TimingStats(object):
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.start_cpu_time = None
        self.end_time = None
        self.end_cpu_time = None

    def start(self):
        self.start_time = time.time()
        self.start_cpu_time = get_cpu_time()

    def stop(self):
        self.end_time = time.time()
        self.end_cpu_time = get_cpu_time()

    def __enter__(self):
        self.start()
        return self

    @property
    def time(self):
        return self.end_time - self.start_time

    @property
    def cpu_time(self):
        return self.end_cpu_time - self.start_cpu_time

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()


class RequestIDContext(object):

    def __init__(self, mode="uuid"):
        self.mode = mode

    def __enter__(self):
        if self.mode == "uuid":
            return generate_request_id_by_uuid()
        else:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class RequestIDMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, mode="uuid"):
        super().__init__(app)
        self.mode = mode

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        with RequestIDContext(mode=self.mode) as request_id:
            if request_id:
                request.scope['x-request-id'] = request_id
            return await call_next(request)


class AccessLogMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, log_name):
        super().__init__(app)
        self.log_name = log_name

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        response = None
        request_id = request.scope.get('x-request-id', None)
        with TimingStats("context") as stats:
            response = await call_next(request)

        # write log to
        if request_id:
            # set response
            response.headers['x-request-id'] = request_id
            # log
            logger = logging.getLogger(self.log_name)
            logger = logging.LoggerAdapter(logger, dict(
                request_id=request_id,
                time_cost=stats.time,
                request_method=request.method,
                request_path=request.url.path,
                request_query=request.url.query,
                request_host=request.url.hostname,
                http_schema=request.url.scheme,
                client_ip=request.client.host,
                client_port=request.client.port,
                response_code=response.status_code
            ))
            logger.info("")

        return response
