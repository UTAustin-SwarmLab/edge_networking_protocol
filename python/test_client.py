import zmq
import time
import common_pb2 as common

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

ping = common.PingServer().SerializeToString()

log = open("timestamps.csv", "w")

while True:
  try:
    start_time = time.time()
    socket.send(ping)
    message = socket.recv()
    stop_time = time.time()

    # print(f"Delay of {stop_time - start_time} s")
    packet_delay_ms = (stop_time - start_time)*1000
    print(f"Delay of {packet_delay_ms} ms")
    log.write(f"{packet_delay_ms},\n")

  except KeyboardInterrupt:
    log.close()
