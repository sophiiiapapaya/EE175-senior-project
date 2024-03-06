import cv2
import socket
import pickle
import struct
import client

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Accept a client connection
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)

# Function to receive file data from client
def receive_file():
    data = b""
    payload_size = struct.calcsize("Q")

    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    file_data = data[:msg_size]

    return file_data

# Function to save received file
def save_file(file_data, file_name):
    with open(file_name, 'wb') as file:
        file.write(file_data)
    print(f"File received and saved as {file_name}")

# Receive file data from client
file_data = receive_file()

# Save received file
file_name = 'sample-media/sample-vid-3.mp4'  # Choose a filename for the received file
save_file(file_data, file_name)

# Play the received media in fullscreen mode using OpenCV
cap = cv2.VideoCapture(file_name)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    cv2.namedWindow("Received Media", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Received Media", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Received Media', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Close connection
client_socket.close()
server_socket.close()

# # Create socket
# class Server_Socket:
#     def __init__(self):
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.host_name = socket.gethostname()
#         try:
#             self.host_ip = socket.gethostbyname(self.host_name)
#             print(f'The {self.host_name} IP Address is {self.host_ip}')
#         except socket.gaierror as e:
#             print(f'Invalid hostname, error raised is {e}')
            
#         self.port = 9999
#         self.socket_addr = (self.host_ip, self.port)
        
#         # Socket Bind
#         self.server_socket.bind(self.socket_addr)

#     def connect_client(self):
#         # Socket Listen
#         self.server_socket.listen(5)
#         print("LISTENING AT:", self.socket_addr)
        
#         # Accept a client connection
#         self.client_socket, self.addr = self.server_socket.accept()
#         print('GOT CONNECTION FROM:', self.addr)
    
#     # Function to save received file
#     def save_file(self, file_data, file_name):
#         with open(file_name, 'wb') as file:
#             file.write(file_data)
#         print(f"File received and saved as {file_name}")
    
#     def play(self,file_path):
#         if self.client_socket: # if connection built
#             # Play the received media in fullscreen mode using OpenCV
#             self.cap = cv2.VideoCapture(file_path)
                        
#             while self.cap.isOpened():
#                 self.ret, self.frame = self.cap.read()
            
#                 if not ret:
#                     break
                
#                 self.codedFrame = pickle.dumps(self.frame)
#                 self.msg = struct.pack("Q", len(self.codedFrame)) + self.codedFrame
#                 try:
#                     self.client_socket.sendall(msg)
#                 except Exception:
#                     print("Connection lost, exiting stream")
#                     self.cap.release()
#                     self.client_socket.close()
                
#                 # cv2.namedWindow("Received Media", cv2.WND_PROP_FULLSCREEN)
#                 # cv2.setWindowProperty("Received Media", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#                 cv2.imshow('Now Playing', self.frame)
#                 if cv2.waitKey(25) & 0xFF == ord('q'):
#                     break
                    
#                 print(self.play_source(file_path)) # Show the source of video
                
#             # Release resources
#             self.cap.release()
#             cv2.destroyAllWindows()
        
#     # def play_source(file_path):
#     #     if file_path == 0: 
#     #         return "started stream"
#     #     else:
#     #         file_name = os.path.basename(file_path)
#     #         file_name, file_type = os.path.splitext(file_name)
#     #         return f"{file_name}{file_type} is playing"

#     # Function to receive file data from client
#     def receive_file(self):
#         self.data = b""
#         self.payload_size = struct.calcsize("Q")
    
#         while len(self.data) < self.payload_size:
#             self.packet = self.client_socket.recv(4 * 1024)
#             if not self.packet:
#                 break
#             self.data += self.packet
    
#         self.packed_msg_size = self.data[:self.payload_size]
#         self.data = self.data[self.payload_size:]
#         self.msg_size = struct.unpack("Q", self.packed_msg_size)[0]
    
#         while len(self.data) < self.msg_size:
#             self.data += self.client_socket.recv(4 * 1024)
    
#         self.file_data = self.data[:self.msg_size]
    
#         return self.file_data
            
#     def close_connection(self):
#         # Close connection
#         self.client_socket.close()
#         self.server_socket.close()
