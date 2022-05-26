import time
import zmq
import struct
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

recv_file = common.ImageFileReq()
send_file = common.ImageFileRecv()

while True:
  #  Wait for next request from client
  message = socket.recv()
  print("Received request!")

  #  Do some 'work'
  recv_file.ParseFromString(message)
  print(recv_file)
  # print("epoch_time: " + str(time_ack))
  # time.sleep(1)

  #  Send reply back to client
  send_file.time_recv = time.time()

  socket.send(send_file.SerializeToString())
  print("Sent protobuf from server!")