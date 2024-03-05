# server.py -- receive frame
import socket
import cv2
import struct
import pickle

def receive_video_path(client_socket):
    video_path = client_socket.recv(1024).decode('utf-8')
    print("Received video path from client:", video_path)
    return video_path

def get_hostname_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except socket.gaierror:
        return "Unable to resolve hostname and IP address."
        
def start_end_device_server():
    # cap = cv2.VideoCapture(video_path)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '0.0.0.0'  # All available interfaces
    server_port = 12345  # Choose a different port for the server
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to client:', addr)
        video_path = receive_video_path(client_socket)
        cap = cv2.VideoCapture(video_path)

        paused = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if not paused:
                cv2.imshow('Video received', frame)
            key = cv2.waitKey(25)
            if key == ord('q'):  # Quit if 'q' is pressed
                break
            elif key == ord('p'):  # Pause if 'p' is pressed
                print("Pausing video.")
                cv2.waitKey(-1)  # Wait until any key is pressed
                paused = True
                print("Video paused.")
            elif key == ord('r'):  # Resume if 'r' is pressed
                paused = False
                print("Resuming video.")
                
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()

    server_socket.close()

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
    # video_path = 'sample-media/sample-vid-3.mp4'
    start_end_device_server()
