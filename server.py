# server.py
import cv2
import socket
import pickle
import struct

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

#Socket Bind
server_socket.bind(socket_address)

#Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

#Accept a client connection
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)

#Video capture
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('sample-media\sample-vid-1.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    message = struct.pack("Q", len(data)) + data
    client_socket.sendall(message)

cap.release()
client_socket.close()
