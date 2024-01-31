# server.py

import socket, pickle, struct
import cv2 as cv
import numpy

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# # If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('Host IP: ', host_ip)
PORT = 9999

server_addr = (host_ip, PORT)
s.bind(server_addr)
s.listen()

# socket accept
while True:
    client_socket, addr = s.accept()
    print(f'Connected by {addr}')
    if client_socket:
        # vid = cv.VideoCapture(0) # Unlike files, the camera has no current position, and CAP_PROP_POS_FRAMES always returns 0
        cv.namedWindow('Transmitting video', cv.WINDOW_NORMAL)
        vid = cv.VideoCapture('sample-media\sample-vid-1.mp4')
        while (vid.isOpened()):
            img,frame = vid.read()
            frame = cv.resize(frame, (1600, 900))
            cv.moveWindow('Transmitting video', 0, 0)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv.imshow('Transmitting video',frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()

