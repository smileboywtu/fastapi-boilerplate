# use wrk to benchmark web application


# install wrk
# git clone https://github.com/wg/wrk.git
# cd wrk
# make

# benchmark web server
# test Get method without SQL
# test Get method with SQL related
./wrk -t 4 -c 300 -d10s http://127.0.0.1:8000/api/v1/user/list


