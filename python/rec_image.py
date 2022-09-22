import zmq
import time
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

image = common.SendImage()
image_ack = common.SendImageAck()

while True:
  message = socket.recv()
#   image.ParseFromString(message)

#   with open("pohans-favorite.png", "wb") as favorite:
#     favorite.write(image.data)

  image_ack.time = time.time()
  serial_image_ack = image_ack.SerializeToString()
  socket.send(serial_image_ack)
