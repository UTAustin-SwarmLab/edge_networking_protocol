import zmq
import time
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

ping = common.PingServer().SerializeToString()

for request in range(10):
  start_time = time.time()
  socket.send(ping)
  message = socket.recv()
  stop_time = time.time()

  # print(f"Delay of {stop_time - start_time} s")
  print(f"Delay of {(stop_time - start_time)*1000} ms")
