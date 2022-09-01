import time
import zmq
import struct
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

ping = common.PingServer().SerializeToString()

while True:
  message = socket.recv()
  socket.send(ping)
