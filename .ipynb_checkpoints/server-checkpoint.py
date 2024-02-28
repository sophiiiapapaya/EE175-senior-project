import cv2
import socket
import pickle
import struct
import client

# Create socket
class Server_Socket:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        try:
            self.host_ip = socket.gethostbyname(self.host_name)
            print(f'The {self.host_name} IP Address is {self.host_ip}')
        except socket.gaierror as e:
            print(f'Invalid hostname, error raised is {e}')
            
        self.port = 9999
        self.socket_addr = (self.host_ip, self.port)
        
        # Socket Bind
        self.server_socket.bind(self.socket_addr)

    def connect_client(self):
        # Socket Listen
        self.server_socket.listen(5)
        print("LISTENING AT:", self.socket_addr)
        
        # Accept a client connection
        self.client_socket, self.addr = self.server_socket.accept()
        print('GOT CONNECTION FROM:', self.addr)
        
    def get_hostIP(self):
        return self.host_ip
    
    # Function to save received file
    def save_file(self, file_data, file_name):
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"File received and saved as {file_name}")
    
    def play(self,file_path):
        if self.client_socket: # if connection built
            # Play the received media in fullscreen mode using OpenCV
            self.cap = cv2.VideoCapture(file_path)
                        
            while self.cap.isOpened():
                self.ret, self.frame = self.cap.read()
            
                if not ret:
                    break
                
                self.codedFrame = pickle.dumps(self.frame)
                self.msg = struct.pack("Q", len(self.codedFrame)) + self.codedFrame
                try:
                    self.client_socket.sendall(msg)
                except Exception:
                    print("Connection lost, exiting stream")
                    self.cap.release()
                    self.client_socket.close()
                
                # cv2.namedWindow("Received Media", cv2.WND_PROP_FULLSCREEN)
                # cv2.setWindowProperty("Received Media", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Now Playing', self.frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                    
                print(self.play_source(file_path)) # Show the source of video
                
            # Release resources
            self.cap.release()
            cv2.destroyAllWindows()
        
    def play_source(file_path):
        if file_path == 0: 
            return "started stream"
        else:
            file_name = os.path.basename(file_path)
            file_name, file_type = os.path.splitext(file_name)
            return f"{file_name}{file_type} is playing"

    # Function to receive file data from client
    def receive_file(self):
        self.data = b""
        self.payload_size = struct.calcsize("Q")
    
        while len(self.data) < self.payload_size:
            self.packet = self.client_socket.recv(4 * 1024)
            if not self.packet:
                break
            self.data += self.packet
    
        self.packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        self.msg_size = struct.unpack("Q", self.packed_msg_size)[0]
    
        while len(self.data) < self.msg_size:
            self.data += self.client_socket.recv(4 * 1024)
    
        self.file_data = self.data[:self.msg_size]
    
        return self.file_data
            
    def close_connection(self):
        # Close connection
        self.client_socket.close()
        self.server_socket.close()
