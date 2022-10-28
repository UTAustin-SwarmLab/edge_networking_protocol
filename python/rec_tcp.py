import zmq
import time
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

image = common.SendBytes()
image_ack = common.SendBytesAck()

while True:
  # Receive the image over the network
  message = socket.recv()

  # Read the bytes received
  image.ParseFromString(message)

  # Create an image ack and the time the image was received and serialize the packets
  image_ack.packet_num = image.packet_num
  serial_image_ack = image_ack.SerializeToString()

  # Send the ack over ZMQ socket to client
  socket.send(serial_image_ack)
