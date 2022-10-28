import time
import zmq
import common_pb2 as common
import argparse
import threading
import itertools
import sys

outbound_messages = {}
DEFAULT_PACKET_SIZE = 64

REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3


parser = argparse.ArgumentParser(description='sending N tcp bytes to server')
parser.add_argument('-n', type=int, help='amount of bytes to send')
args = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://10.157.30.72:5555")

send_image = common.SendBytes()

if (args.n == None):
  send_image.data = bytes([0xFF] * DEFAULT_PACKET_SIZE)
else:
  send_image.data = bytes([0xFF] * args.n)

print("Starting client!")

image_ack = common.SendImageAck()

log = open("timestamps.csv", "w")



def receive_from_server():
  while True:
    # Receive ack for the image being received
    message = socket.recv()
    image_ack.ParseFromString(message)

    # Stop measuring time
    end_time = time.time()

    start_time = outbound_messages[image_ack.packet_num]

    # Log the time
    packet_delay_ms = (end_time - start_time) * 1000
    print(f"This is duration: {packet_delay_ms} ms")
    log.write(f"{packet_delay_ms},\n")


receive_thread = threading.Thread(target = receive_from_server)
receive_thread.start()


def send_packet(packet_num):
  send_image.packet_num = packet_num
  serial_send_image = send_image.SerializeToString()

  # Start measuring time
  outbound_messages[packet_num] = time.time()
  socket.send(serial_send_image)

packet_num = 0

for sequence in itertools.count():
  send_packet(packet_num)

  retries_left = REQUEST_RETRIES
  while True:
    if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
      reply = socket.recv()
      if int(reply) == sequence:
        retries_left = REQUEST_RETRIES
        break
      else:
        print(f"Malformed reply from server: {reply}")
        continue
    
    retries_left -= 1
    # Socket is confused. Close and remove it.
    socket.setsockopt(zmq.LINGER, 0)
    socket.close()
    if retries_left == 0:
      # logging.error("Server seems to be offline, abandoning")
      sys.exit()

    # logging.info("Reconnecting to server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://10.157.30.72:5555")
    # logging.info("Resending (%s)", request)
    send_packet(packet_num)



# try:
#   packet_num = 1

#   while True:
    

#     # Send image over ZMQ socket
#     socket.send(serial_send_image)

#     packet_num += 1

# except KeyboardInterrupt:
#   log.close()

