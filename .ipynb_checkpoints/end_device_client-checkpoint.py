# server.py -- receive frame
import socket
import cv2
import struct
import pickle
import numpy as np
import os, subprocess
import threading
    
def get_hostname_ip(server_socket):
    try:
        hostname = socket.gethostname()
        # ip_address = socket.gethostbyname(hostname)
        ip_address = str(os.system('hostname -I'))
        return hostname, ip_address
    except socket.gaierror:
        return "Unable to resolve hostname and IP address."
        
def start_end_device_server():
    global cap_flag, socket_flag
    server_ip = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.strip()
    print(server_ip)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = '10.13.229.231'
    # server_ip = '0.0.0.0'  # All available interfaces on the same machine, for testing

    server_port = 12345  # Choose a different port for the server
    server_socket.bind((server_ip, server_port))
    server_socket.listen()  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")

    while True: # while listening for connection
        # wait and accept new connection
        client_socket, addr = server_socket.accept() 
        print('Connected to client:', addr)
        
        cap_flag = False # shows cv2.VideoCapture()
        socket_flag = True # destroy window when it turns to false
        while True: # while a socket is accepted
            black_scrn = threading.Thread(target=black_screen, args=())
            # black_scrn.daemon = True # A process will exit if only daemon threads are running (or if no threads are running).
            black_scrn.start()
            
            message = receive_message(client_socket) # get filename from client
    
            msg = message.split() # array
            # print(msg[0])
            if msg[0] == "Sending":
                # Save received file.
                file_name = msg[1]
                file_data = receive_file(client_socket)        
                save_file(file_data, file_name) # write file(s) to server machine
                # save_file(file_name, client_socket) # write file(s) to server machine
                recv_msg = f"{file_name} saved"
                client_socket.sendall(recv_msg.encode('utf-8'))
            
            if msg[0] == "Playing" or msg[0] == "Quit" or msg[0] == "Play" or msg[0] == "Pause":
                if msg[0] == "Playing":
                    file_name = msg[1]
    
                cmd = msg[0]
                playback(file_name, cmd)
    
        client_socket.close()
        socket_flag = False
        cv2.destroyAllWindows()

    server_socket.close()

def receive_message(client_socket):
    message = client_socket.recv(1024).decode('utf-8')
    print("Message received from client:", message)
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
    # n = 0
    # file_data = client_socket.recv(1024)
    with open(file_name, 'wb') as file:
        file.write(file_data)
        # n += 1
        # while file_data:                
        #     file.write(file_data)
        #     file_data = client_socket.recv(1024)
    print(f"File received and saved as {file_name}")  
    

def black_screen():
    global socket_flag
    while socket_flag:
        bg = np.zeros((720, 1280, 3), np.uint8)  # Black screen frame
        cv2.namedWindow('Black screen', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Black screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Black screen', bg)
        # waits for user to press any key 
        # (this is necessary to avoid Python kernel form crashing) 
        cv2.waitKey(0) 
        print("Black screen on")
        
    cv2.destroyWindow('Black screen')


def playback(file_name, cmd):
    global cap_flag
    paused = False
    # Play the received media in fullscreen mode using OpenCV
    if cap_flag:
        cap.release()
        print(f"Closing current video, play {file_name}")

    cap = cv2.VideoCapture(file_name)
    file_name, file_type = os.path.splitext(file_name)

    while cap.isOpened():
        cap_flag = True 
        ret, frame = cap.read()
        if not ret:
            break
        if not paused:
            cv2.namedWindow('Video received', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Video received', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Video received', frame)

        if cmd == "Quit":  # Quit if 'q' is pressed
            print("Quitting video")
            break
        elif cmd == "Pause":  # Pause if 'p' is pressed
            print("Pausing video.")
            cv2.waitKey(-1)  # Wait until any key is pressed
            paused = True
            print("Video paused.")
        elif cmd == "Play":  # Resume if 'r' is pressed
            paused = False
            print("Resuming video.")
        else:
            cv2.waitKey(25) & 0xFF 

    cap_flag = False 
    cap.release()
    cv2.destroyWindow('Video received')

if __name__ == "__main__":
    # video_path = 'sample-media/sample-vid-3.mp4'
    start_end_device_server()
