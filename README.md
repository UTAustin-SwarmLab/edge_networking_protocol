# tiny_networking_protocol
pip3 install pyzmq \
pip3 install protobuf \
protoc -I=./ --python_out=proto/ ./common.proto
cp ../proto/common_pb2.py ./
