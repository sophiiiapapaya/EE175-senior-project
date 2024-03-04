# gui_client.py -- send frames
import socket
import tkinter as tk
import cv2
import pickle
import struct
import end_device_client

def create_socket(end_device_ip):
    global client_socket
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        # Specify the end device's port
        end_device_port = 12345
            
        # Connect to the end device
        client_socket.connect((end_device_ip, end_device_port))

        # message = input("Enter message to send to server: ")
        # message_to_end_device("GUI Client received message")

    except Exception as e:
        print("Error:", e)

# send media
# send_media_cv2.py
def media_to_end_device(file_path):
    global client_socket, cap
    try:
        cap = cv2.VideoCapture(file_path)

        # client_socket.close()
    except Exception as e:
        print("Error:", e)

def playback_ctrl(is_playing, cmd):
    global client_socket, cap
    try:            
        while cap.isOpened():
            if is_playing:
                ret, frame = cap.read()
                
                if not ret:
                    print("Video finished.")
                    break
                    
                codedFrame = pickle.dumps(frame)
                msg = struct.pack("Q", len(codedFrame)) + codedFrame
                try:
                    client_socket.sendall(msg)
                except Exception:
                    print("Connection lost, exiting stream")
                    cap.release()
                    client_socket.close()
    
                cv2.imshow('Now Playing', frame)
                a
            key = cv2.waitKey(25) & 0xFF
            if key == ord(cmd): # cmd == 'q', quit video
                break
            elif key == ord(cmd): # cmd == 'p', pause video
                if not is_playing:
                    is_playing = True
                else: 
                    is_playing = False
                    message = "Video paused"
                    client_socket.sendall(message.encode('utf-8'))
                    cv2.waitKey(-1) # wait until any key is pressed ('r' assigned)

            if is_playing:
                message = "Playing video"
                client_socket.sendall(message.encode('utf-8'))
                
    except Exception as e:
        print("Error:", e)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()
    
# send message 
def message_to_end_device(message):
    try:
        # Send message to the end device
        client_socket.sendall(message.encode('utf-8'))
    
            
        # Receive response from the end device (if needed)
        response = client_socket.recv(1024).decode('utf-8')
        print("Response from end device:", response)
            
        # Close the connection
        client_socket.close()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # create_gui()
    create_socket()

