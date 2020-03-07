# Fastapi Boilerplate

Fastapi is a modern Python web framework for writting web apis. it's fast and 
featured.

see more detail about [fastapi](https://github.com/tiangolo/fastapi).

this Boilerplate is based on Fastapi framework with some common module for fast 
python restapi development.

# Feature

- fully async support: function, database, background task
- celery distribute task support
- distribute request id support
- feature log support
- in-memory zmq support for multi-process task
- async postgresql support
- support sql template programing
- docker support 
- api doc
- api test

# why celery

Fastapi provide a way to give background task, but is not really cover all ways when we develop other web application, the one buildin fastapi is good at io-bound task but not cpu bound task. when we define many io-bound task inside web application, we will make the api server slower. we need some way to make web server and tasks isolation.

# why distribute request id

even you use `UUID4` as request id, it's not suitable for high cocurrent api server. you will get same request id for a batch of requests, it's bad for log analyse and debug.

# why zmq

`zmq` gains high performance and is very simple. use zmq to communicate with multiprocess task is a good way. 

we usally use zmq queue do tasks:
- send multi-process log to single file
- send multi-process redis writting data using single redis client

# why docker

docker is a good way to distribute application on different os environment, it makes our final web application deployment easy.

# performance

we choose `wrk` as a load test tool. it very simple and fast. see more detail inside `benchmark.sh`.

# run

we use make tool to manage other web server.

``` shell
# build the docker container
make build

# test web application
make test

# run docker container
make run

# stop docker container
make stop
```

# sql write

if you need to write your own sql function, you need to read the doc first, [anosql query options](https://anosql.readthedocs.io/en/latest/defining_queries.html#query-operations).

-  Execute SQL script statements with #
-  Insert/Update/Delete Many with *!
-  Insert Returning with <!
-  Insert/Update/Delete with !
-  Flat return single row data with ?

for example:
```sql
-- name: publish_blog<!
insert into blogs(userid, title, content) values (:userid, :title, :content);

-- name: insert_many*!
insert into blogs(userid, title, content, published) values (?, ?, ?, ?);
```