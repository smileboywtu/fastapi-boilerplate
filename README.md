# Fastapi 开发模版

Fastapi 使用了 Python 的异步接口特性，可以提升比较多的性能，另外 API 使用起来比较简洁直观，更加符合开发者的习惯。

Fastapi 更多特性参考[文档](https://github.com/tiangolo/fastapi)。

本模版在 Fastapi 的功能基础上集成了更多常用的功能，用户可以根据自己的需求进行删减，删减比增加可能更加容易一些。

# 特性支持

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

## hardware information

aliyun ECS 16C 32G 2.4G with 8 process.

## test with postgres read mode

run test 4 threads 300 concurrency with postgres read:

```shell
./wrk -t 4 -c 300 -d10s http://127.0.0.1:8000/api/v1/user/list
Running 10s test @ http://127.0.0.1:8000/api/v1/user/list
  4 threads and 300 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    66.94ms   49.40ms 604.50ms   73.71%
    Req/Sec     1.22k   252.57     1.87k    64.75%
  48659 requests in 10.10s, 11.09MB read
Requests/sec:   4819.52
Transfer/sec:      1.10MB
```
## test with redis write mode

run test 4 threads 300 concurrency with redis write:
```shell
./wrk -t 4 -c 400 -d10s http://127.0.0.1:8000/api/v1/user/counter
Running 10s test @ http://127.0.0.1:8000/api/v1/user/counter
  4 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    58.08ms  140.53ms   1.05s    94.98%
    Req/Sec     4.04k     1.95k    8.53k    66.00%
  160779 requests in 10.04s, 31.89MB read
  Socket errors: connect 0, read 1820, write 0, timeout 0
Requests/sec:  16012.11
Transfer/sec:      3.18MB
```

## test with echo server mode
run test 4 threads 300 concurrency with echo server:
```shell
./wrk -t 4 -c 400 -d10s http://127.0.0.1:8000/api/v1/user/greeting
Running 10s test @ http://127.0.0.1:8000/api/v1/user/greeting
  4 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    33.45ms   77.33ms   1.01s    96.80%
    Req/Sec     5.35k     2.66k   12.48k    66.75%
  212805 requests in 10.05s, 43.43MB read
  Socket errors: connect 0, read 2078, write 0, timeout 0
Requests/sec:  21179.64
Transfer/sec:      4.32MB
```

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

# config

you can write you business config inside `config.py` file, other environments config use by components you can write it into .envs.production directory, please look at the two sample config file:
- sample.fastapi
- sameple.postgres

config and rename it without sample(.fastapi .postgres) and move it into .envs/.production directory.

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