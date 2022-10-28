import zmq
import time
import common_pb2 as common

context = zmq.Context().instance()
radio = context.socket(zmq.RADIO)
dish = context.socket(zmq.DISH)
dish.rcvtimeo = 1000

dish.bind('udp://*:5556')
dish.join('numbers')
radio.connect("tcp://10.157.30.72:5557")

image = common.SendImage()
image_ack = common.SendImageAck()

while True:
  # Receive the image over the network
  message = dish.recv(copy=False)

  # Create an image ack and the time the image was received and serialize the packets
  image_ack.time = time.time()
  serial_image_ack = image_ack.SerializeToString()

  # Send the ack over ZMQ socket to client
  radio.send(serial_image_ack)
