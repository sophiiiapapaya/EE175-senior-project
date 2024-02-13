
# Client.py
import cv2
import socket
import pickle
import struct

#Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '192.168.1.100'  # Change SERVER_IP to the server's IP address

host_ip = '10.13.26.224'
port = 9999

client_socket.connect((host_ip, port))
data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(41024)  # Receiving data
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(41024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize frame
    frame = pickle.loads(frame_data)
    cv2.namedWindow("Receiving Video", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Receiving Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Receiving Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()