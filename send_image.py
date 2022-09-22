import time
import zmq
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

send_image = common.SendImage()
with open("pohan.jpeg", "rb") as image_bytes:
  send_image.data = image_bytes.read()
image = send_image.SerializeToString()

# print("Starting server!")

image_ack = common.SendImageAck()

while True:
  start_time = time.time()
  socket.send(image)
  message = socket.recv()
  image_ack.ParseFromString(message)
  end_time = time.time()

  print(f"Image acked at {image_ack.time}")
  print(f"This is duration: {end_time - start_time}")

