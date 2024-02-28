# Client.py
import cv2
import socket
import pickle
import struct
import server

class Client_Socket:
    def __init__(self, hostIP):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_ip = hostIP  # Change SERVER_IP to the server's IP address
        self.port = 9999
        self.socket_addr = (self.host_ip, self.port)
        self.client_socket.connect(self.socket_addr)
    
    def receive_file(self):
        data = b""
        payload_size = struct.calcsize("Q")
    
        while True:
            while len(data) < payload_size:
                packet = self.client_socket.recv(262144*1024)  # Receiving data
                if not packet:
                    break
                data += packet
        
            if len(data) < payload_size:
                continue  # Continue receiving until enough data is received
        
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
        
            while len(data) < msg_size:
                packet = self.client_socket.recv(262144*1024)
                if not packet:
                    break
                data += packet
        
            if len(data) < msg_size:
                continue  # Continue receiving until complete message is received
        
            frame_data = data[:msg_size]
            data = data[msg_size:]
        
            # Deserialize frame
            frame = pickle.loads(frame_data)
        
            cv2.namedWindow("Receiving Video", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Receiving Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
            cv2.imshow("Receiving Video", frame)
        
            key = cv2.waitKey(25) & 0xFF
        
            if key == ord('q'):
                break
    def close_connection(self):
        self.client_socket.close()
