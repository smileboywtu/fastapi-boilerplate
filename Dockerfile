FROM python:3.7-alpine

WORKDIR /app

RUN copy requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "run:app_instance", "-w", "8", "-k", "uvicorn.workers.UvicornWorker" ]