---
title: how to log something
date: 2020-03-08 10:12:17 +08
---


如何在 fastapi 中输出 log 到文件？

目前官方的文档中并没有说明如何处理 log 日志，因为我们将来生产的时候，会多线程部署，那么这个时候就需要多线程，多进程写日志，这些是一个非常麻烦的事情，多进程同时写一个文件会出现文件锁的问题。

一个方法是根据线程号把日志写入到多个文件中，这样做是可行的，但是给收集带了不少麻烦。

我们 socket log handler, 这样不仅可以解决多进程的问题，还可以保证我们事后收集日志文件变得简单，直接和 syslog 对接。

这个地方我们需要在日志中添加很多额外的字段，另外因为 fastapi 没有基本的日志模块，所以我们需要自己处理，这里我们以 access log 为例：

初始化 logger:

```python
def config_socket_logger(logger_name, log_format, log_level, socket_host="127.0.0.1", socket_port=514):
    """
    config socket logger

    :param logger_name:
    :param log_format:
    :param log_level:
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    handler = logging.handlers.SocketHandler(socket_host,
                                             514 or logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger
```

基本的 formmater:
```shell
access_log_format = "%(asctime)s %(levelname)s %(request_id)s %(time_cost).2f " \
                    "%(request_method)s %(request_path)s %(response_code)s"
```

需要添加的字段：

- request_id
- request_method
- request_path
- time_cost
- response_code

其余的随着业务需要也可以定制，具体你需要先把需要的字段在 middleware 中准备好：

```python
class AccessLogMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, log_name):
        super().__init__(app)
        self.log_name = log_name

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        response = None
        with TimingStats("context") as stats:
            response = await call_next(request)

        # write log to
        logger = logging.getLogger(self.log_name)
        logger = logging.LoggerAdapter(logger, dict(
            request_id=request.request_id,
            time_cost=stats.time,
            request_method=request.method,
            request_path=request.base_url.path,
            response_code=response.status_code
        ))
        logger.info("")

        return response
```

使用 logger 的 adapter 来为每个 log record 增加额外的字段属性。

因为 request_id 是我们必须的，所以我们必须在调用 log middleware 给 request 增加一个 request_id 属性：

```python
class RequestIDContext(object):

    def __init__(self, mode="uuid"):
        self.mode = mode

    def __enter__(self):
        if self.mode == "uuid":
            return generate_request_id_by_uuid()
        else:
            return ""

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class RequestIDMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, mode="uuid"):
        super().__init__(app)
        self.mode = mode

    def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        with RequestIDContext() as request_id:
            request.request_id = request_id
            return await call_next(request)
```

通过另外一个 middleware 来实现。因为 fastapi 中所有的 middleware 是按照添加的先后顺序执行的，所以这个 request_id middleware 需要优于 log middleware 添加。