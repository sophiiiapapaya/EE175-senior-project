# gui_client.py -- send frames
import socket
import tkinter as tk
import cv2
import pickle
import struct

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

def is_playing():
    global cap
    try:        
        if cap.isOpened():
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)

# send media
# send_media_cv2.py
def media_to_end_device(file_path):
    global client_socket, cap
    try:        
        if file_path == "Message from GUI client":
            message_to_end_device(file_path)
        else:
            cap = cv2.VideoCapture(file_path)
            paused = False
            client_socket.sendall(file_path.encode('utf-8'))
            while cap.isOpened():
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        print("Video finished.")
                        break
                        
                    # codedFrame = pickle.dumps(frame)
                    # msg = struct.pack("Q", len(codedFrame)) + codedFrame
                    # try:
                    #     client_socket.sendall(msg)
                    # except Exception:
                    #     print("Connection lost, exiting stream")
                    #     cap.release()
                    #     client_socket.close()
        
                    cv2.imshow('Video sending', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    message = "Quit"
                    print(message)
                    client_socket.sendall(message.encode('utf-8'))
                    break
                elif cv2.waitKey(25) & 0xFF == ord('p'):
                    if paused:
                        paused = False
                        message = "Play"
                    else:
                        paused = True
                        message = "Pause"
                        print(message)
                        cv2.waitKey(-1) # wait until any key is pressed
                        if key == ord(cmd):  # 'p' Pause or resume the video
                            paused = False
                            message = "Play"
                    client_socket.sendall(message.encode('utf-8'))

            # Release resources
            cap.release()
            cv2.destroyAllWindows()
            client_socket.close()
        
    except Exception as e:
        print("Error:", e)

# def playback_ctrl(client_socket, cap, paused):
#     try:            
#         while cap.isOpened():
#             if not paused:
#                 ret, frame = cap.read()
#                 if not ret:
#                     print("Video finished.")
#                     break
                    
#                 # codedFrame = pickle.dumps(frame)
#                 # msg = struct.pack("Q", len(codedFrame)) + codedFrame
#                 # try:
#                 #     client_socket.sendall(msg)
#                 # except Exception:
#                 #     print("Connection lost, exiting stream")
#                 #     cap.release()
#                 #     client_socket.close()
    
#                 cv2.imshow('Video sending', frame)
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 message = "Quit"
#                 print(message)
#                 client_socket.sendall(message.encode('utf-8'))
#                 break
#             elif cv2.waitKey(25) & 0xFF == ord('p'):
#                 if paused:
#                     paused = False
#                     message = "Play"
#                 else:
#                     paused = True
#                     message = "Pause"
#                     print(message)
#                     cv2.waitKey(-1) # wait until any key is pressed
#                     if key == ord(cmd):  # 'p' Pause or resume the video
#                         paused = False
#                         message = "Play"
#                 client_socket.sendall(message.encode('utf-8'))

#         # print("cap closed")
                
#     except Exception as e:
#         print("Error:", e)

#     # Release resources
#     cap.release()
#     cv2.destroyAllWindows()
#     client_socket.close()
    
# send message 
def message_to_end_device(message):
    try:
        # Send message to the end device
        client_socket.sendall(message.encode('utf-8'))
    
            
        # Receive response from the end device (if needed)
        response = client_socket.recv(1024).decode('utf-8')
        print("Response from end device:", response)
        
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # create_gui()
    create_socket()

