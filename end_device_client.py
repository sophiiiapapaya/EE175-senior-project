# server.py -- receive frame
import socket
import cv2
import struct
import pickle
import numpy as np

def get_hostname_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except socket.gaierror:
        return "Unable to resolve hostname and IP address."
        
def start_end_device_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = '10.13.229.231'
    server_ip = '0.0.0.0'  # All available interfaces on the same machine, for testing
    server_port = 12345  # Choose a different port for the server
    server_socket.bind((server_ip, server_port))
    server_socket.listen()  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")
    
    client_socket, addr = server_socket.accept() # Listening from the same client
    print('Connected to client:', addr)

    while True:
        
        # message = receive_message(client_socket) # get filename from client
        # print(message)

        # if not message is type file data:
        file_data = receive_file(client_socket)

        message = receive_message(client_socket) # get filename from client
        print(message)

        # elif message is type file_name:

        # Save received file.
        file_name = message
        save_file(file_data, file_name) # write file(s) to server machine. need to return data?

        cmd = message
        playback(file_name, cmd)
        
        # # Play the received media in fullscreen mode using OpenCV
        # cap = cv2.VideoCapture(file_name)

        # paused = False

        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     if not ret:
        #         break
        #     if not paused:
        #         cv2.namedWindow('Video received', cv2.WND_PROP_FULLSCREEN)
        #         cv2.setWindowProperty('Video received', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        #         cv2.imshow('Video received', frame)
                
        #     key = cv2.waitKey(25)
        #     # try: if (key == ord(cmd)) and (cmd == 'q'):
        #     if key == ord('q'):  # Quit if 'q' is pressed
        #         break
        #     elif key == ord('p'):  # Pause if 'p' is pressed
        #         print("Pausing video.")
        #         cv2.waitKey(-1)  # Wait until any key is pressed
        #         paused = True
        #         print("Video paused.")
        #     elif key == ord('r'):  # Resume if 'r' is pressed
        #         paused = False
        #         print("Resuming video.")
                
        # cap.release()
        # cv2.destroyAllWindows()
    
    client_socket.close()

    server_socket.close()

def receive_message(client_socket):
    message = client_socket.recv(1024).decode('utf-8')
    print("Received from client:", message)
    return message

def receive_file(client_socket):
    data = b""
    payload_size = struct.calcsize("Q")

    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)  # Receiving data
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
        
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    # data = data[msg_size:]

    # Deserialize frame
    # frame = pickle.loads(frame_data)  

    return frame_data

def save_file(file_data, file_name):
    with open(file_name, 'wb') as file:
        file.write(file_data)
    print(f"File received and saved as {file_name}")  

def playback(file_name, cmd):
    # Play the received media in fullscreen mode using OpenCV
    cap = cv2.VideoCapture(file_name)

    paused = False
    black_screen = False

    while True:
        if black_screen:
            frame = np.zeros((480, 640, 3), np.uint8)  # Black screen frame
            cv2.imshow('Video received', frame)
            cv2.setWindowProperty('Video received', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            ret, frame = cap.read()
            if not ret:
                # If the video ends, set black screen flag to True
                black_screen = True
                continue  # Skip displaying the last frame
            else:
                # Display the frame if the video is playing
                cv2.namedWindow('Video received', cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty('Video received', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Video received', frame)
                
        key = cv2.waitKey(25)
        if key == ord('q'):  #Quit if 'q' is pressed
            break
        elif key == ord('p'):  #Pause if 'p' is pressed
            print("Pausing video.")
            cv2.waitKey(-1)  #Wait until any key is pressed
            paused = True
            print("Video paused.")
        elif key == ord('r'):  #Resume if 'r' is pressed
            paused = False
            print("Resuming video.")
        elif key == ord('n'):  #Enter black screen state if 'n' is pressed
            black_screen = True
            print("Entered black screen state. Waiting for another file to be uploaded.")
                
    cap.release()
    cv2.destroyAllWindows()  # Ensure the window is closed when 'q' is pressed
  # Ensure the window is closed when 'q' is pressed


if __name__ == "__main__":
    # video_path = 'sample-media/sample-vid-3.mp4'
    start_end_device_server()
