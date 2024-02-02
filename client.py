# client.py

import socket, pickle, struct
import cv2 as cv
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.13.27.104'
PORT = 9999
s.connect((host_ip, PORT))
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = s.recv(4*1024)
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]

    while len(data) < msg_size:
        data += s.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv.imshow("Received", frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
s.close()