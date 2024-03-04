# Client.py (receiving)
import cv2
import socket
import pickle
import struct
import server

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.13.170.2'  # Change SERVER_IP to the server's IP address
port = 9999

client_socket.connect((host_ip, port))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(262144*1024)  # Receiving data
        if not packet:
            break
        data += packet

    if len(data) < payload_size:
        continue  # Continue receiving until enough data is received

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        packet = client_socket.recv(262144*1024)
        if not packet:
            break
        data += packet

    if len(data) < msg_size:
        continue  # Continue receiving until complete message is received

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize frame
    frame = pickle.loads(frame_data)

    # cv2.namedWindow("Receiving Video", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("Receiving Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("Receiving Video", frame)

    key = cv2.waitKey(25) & 0xFF

    if key == ord('q'):
        break

client_socket.close()

# class Client_Socket:
#     # def __init__(self, hostIP):
#     #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #     self.host_ip = hostIP  # Change SERVER_IP to the server's IP address
#     #     self.port = 9999
#     #     self.socket_addr = (self.host_ip, self.port)
#     #     self.client_socket.connect(self.socket_addr)
    
#     def receive_file(self):
#         data = b"" # binary data
#         payload_size = struct.calcsize("Q")
    
#         while True:
#             while len(data) < payload_size:
#                 packet = self.client_socket.recv(262144*1024) # Receiving data
#                 if not packet:
#                     break
#                 data += packet
        
#             if len(data) < payload_size:
#                 continue  # Continue receiving until enough data is received
        
#             packed_msg_size = data[:payload_size]
#             data = data[payload_size:]
#             msg_size = struct.unpack("Q", packed_msg_size)[0]
        
#             while len(data) < msg_size:
#                 packet = self.client_socket.recv(262144*1024)
#                 if not packet:
#                     break
#                 data += packet
        
#             if len(data) < msg_size:
#                 continue  # Continue receiving until complete message is received
        
#             frame_data = data[:msg_size]
#             data = data[msg_size:]
        
#             # Deserialize frame
#             frame = pickle.loads(frame_data)
        
#             cv2.namedWindow("Receiving Video", cv2.WND_PROP_FULLSCREEN)
#             cv2.setWindowProperty("Receiving Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
#             cv2.imshow("Receiving Video", frame)
        
#             key = cv2.waitKey(25) & 0xFF
        
#             if key == ord('q'):
#                 break # stop and quit window

#             if key == ord('p'):
#                 cv2.waitKey(-1) # wait until any key is pressed
                
#     def close_connection(self):
#         self.client_socket.close()
