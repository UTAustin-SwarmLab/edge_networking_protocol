import time
import zmq
import common_pb2 as common
import argparse

DEFAULT_PACKET_SIZE = 64

parser = argparse.ArgumentParser(description='sending N tcp bytes to server')
parser.add_argument('-n', type=int, help='amount of bytes to send')
args = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.157.30.72:5555")

send_image = common.SendImage()

if (args.n == None):
  send_image.data = bytes([0xFF] * DEFAULT_PACKET_SIZE)
else:
  send_image.data = bytes([0xFF] * args.n)

serial_send_image = send_image.SerializeToString()

print("Starting client!")

image_ack = common.SendImageAck()

log = open("timestamps.csv", "w")

try:
  while True:
    # Start measuring time
    start_time = time.time()

    # Send image over ZMQ socket
    socket.send(serial_send_image)

    # Receive ack for the image being received
    message = socket.recv()
    image_ack.ParseFromString(message)

    # Stop measuring time
    end_time = time.time()

    # Log the time
    print(f"Image acked at {image_ack.time}")
    packet_delay_ms = (end_time - start_time) * 1000
    print(f"This is duration: {packet_delay_ms} ms")
    log.write(f"{packet_delay_ms},\n")

except KeyboardInterrupt:
  log.close()

