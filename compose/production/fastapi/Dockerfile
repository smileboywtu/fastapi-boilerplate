FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir ~/.pip/ && echo -e \
    "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > \
    ~/.pip/pip.conf && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' \
    /etc/apk/repositories

# install gcc
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev alpine-sdk libuv

# create user
RUN addgroup -S fastapi \
    && adduser -S -G fastapi fastapi

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# add startup entrypoint
COPY ./compose/production/fastapi/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown fastapi /entrypoint

COPY ./compose/production/fastapi/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown fastapi /start

COPY ./compose/production/fastapi/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown fastapi /start-celeryworker

COPY ./compose/production/fastapi/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat
RUN chown fastapi /start-celerybeat

COPY ./compose/production/fastapi/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY ./compose/production/fastapi/log_tcp_server/start /start-logtcpserver
RUN sed -i 's/\r//' /start-logtcpserver
RUN chmod +x /start-logtcpserver

COPY . /app

RUN chown -R fastapi /app

USER fastapi

#EXPOSE 8000

ENTRYPOINT ["/entrypoint"]

#ENTRYPOINT [ "gunicorn", "run:app_instance", "-w", "8", "-k", "uvicorn.workers.UvicornWorker" ]