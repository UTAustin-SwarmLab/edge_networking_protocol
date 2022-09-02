import zmq
import time
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

image = SendImage()
image_ack = common.SendImageAck()

while True:
  message = socket.recv()
#   image.ParseFromString(message)

#   with open("pohans-favorite.png", "wb") as favorite:
#     favorite.write(image.data)

  image_ack.time = time.time()
  image_ack.SerializeToString()
  socket.send(image_ack)
