# end_device_client.py -- receive frames
import socket
import cv2
import pickle
import struct

WIN_NAME = "Video received"

# def receive_msg(client_socket):
#     # Receive data from GUI client
#     data = client_socket.recv(1024).decode('utf-8')
#     if not data:
#         return
#     print("Received from GUI client:", data)
#     if data == "Message from GUI client":
#         # Send response back to GUI client
#         response = "Message received by end device"
#         client_socket.sendall(response.encode('utf-8'))
#     else:
#         return data

def start_end_device_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '0.0.0.0' # All availabe interfaces
    server_port = 12345  # Choose a different port for the server
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to GUI client:', addr)
        # data = receive_msg(client_socket)
        video_path = client_socket.recv(1024).decode('utf-8')
        print("Received from GUI client:",video_path)
        cap = cv2.VideoCapture(video_path)
        
        paused = False            
                
        while cap.isOpened():
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("Video finished.")
                    break
                            
                # Full screen
                cv2.namedWindow(WIN_NAME, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(WIN_NAME, frame)
                
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message == "Pause":
                cv2.waitKey(-1) # wait until any key is pressed
                paused = True
            elif message == "Play":
                cv2.waitKey(25) & 0xFF == ord('p')
                paused = False
            elif message == "Quit":
                break
                    
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()
    server_socket.close()

def get_hostname_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except socket.gaierror:
        return "Unable to resolve hostname and IP address."

# def receive_media(paused):
    # data = b""
    # payload_size = struct.calcsize("Q")

    # while len(data) < payload_size:
    #     packet = client_socket.recv(262144*1024)  # Receiving data
    #     if not packet:
    #         break
    #     data += packet

    # if len(data) < payload_size:
    #     continue  # Continue receiving until enough data is received
        
    # packed_msg_size = data[:payload_size]
    # data = data[payload_size:]
    # msg_size = struct.unpack("Q", packed_msg_size)[0]
        
    # while len(data) < msg_size:
    #     packet = client_socket.recv(262144*1024)
    #     if not packet:
    #         break
    #     data += packet
        
    # if len(data) < msg_size:
    #     continue  # Continue receiving until complete message is received
        
    # frame_data = data[:msg_size]
    # data = data[msg_size:]
        
    # # Deserialize frame
    # frame = pickle.loads(frame_data)

    # # Full screen
    # cv2.namedWindow(WIN_NAME, cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # # New window
    # cv2.imshow(WIN_NAME, frame)
    

if __name__ == "__main__":
    start_end_device_server()
