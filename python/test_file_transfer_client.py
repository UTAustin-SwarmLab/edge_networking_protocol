#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time
import struct
import common_pb2 as common

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

send_file = common.ImageFileReq()
recv_file = common.ImageFileRecv()

file = open("../src/dummy.txt", "rb")

send_file.data = file.read()

send_file.time_sent = time.time()

print("Sending request at: " + str(send_file.time_sent))
socket.send(send_file.SerializeToString())

#  Get the reply.
message = socket.recv()

recv_file.ParseFromString(message)

print(recv_file)
print("Delay of " + str(recv_file.time_recv - send_file.time_sent) + "\n")