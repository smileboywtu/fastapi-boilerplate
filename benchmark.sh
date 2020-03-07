# use wrk to benchmark web application


# install wrk
# git clone https://github.com/wg/wrk.git
# cd wrk
# make

# benchmark web server
# test Get method without SQL
# test Get method with SQL related
./wrk -t 4 -c 500 -s 60s http://

