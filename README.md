# tiny_networking_protocol

Installing the required python libraries: \
pip3 install pyzmq \
pip3 install protobuf==3.19.0 \
apt install protobuf-compiler \

Just make sure to run the getting_started script in the root dir \

Added send_sync_tcp.py and rec_sync_tcp.py \
python3 send_sync_tcp.py -n 100 \
The n parameter allows you to specify amount of bytes to send \

Tried to get asynchronous protocol working with TCP, unsure why it isn't working properly \
ZMQ mentioned that it might be better to use a lazy pirate algorithm, so I've tried to implement that in send_tcp and rec_tcp. \
I didn't have enough time to flesh it completely, but I think 1-2 lines of code might need to be moved around \

Otherwise, to run UDP (Radio, Dish), it requires libzmq to be installed with draft support \
was having problems installing and linking the library to do so... \

