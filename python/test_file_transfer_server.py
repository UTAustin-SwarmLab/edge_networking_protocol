import zmq
import common_pb2 as common
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

recv_file = common.ImageFileReq()
send_file = common.ImageFileRecv()

while True:
  message = socket.recv()
  print("Received request!")

  #  Do some 'work'
  recv_file.ParseFromString(message)
  print(recv_file)
  file = open("./files_received/"+str(recv_file.time_sent), "wb")
  file.write(recv_file.data)
  file.close()
  print("Saved file to: ./files_received/"+str(recv_file.time_sent))

  #  Send reply back to client
  send_file.time_recv = time.time()

  socket.send(send_file.SerializeToString())
  print("Sent protobuf from server!")
