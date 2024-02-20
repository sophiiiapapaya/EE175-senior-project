import cv2
import socket
import pickle
import struct

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
file_name = 'received_media.mp4'  # Choose a filename for the received file
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
