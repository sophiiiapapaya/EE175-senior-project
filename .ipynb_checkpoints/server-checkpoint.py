import socket
import cv2

def start_end_device_server(video_path):
    cap = cv2.VideoCapture(video_path)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '0.0.0.0'  # All available interfaces
    server_port = 12345  # Choose a different port for the server
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to client:', addr)
        paused = False

        while cap.isOpened():
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow('Video received', frame)
                
            key = cv2.waitKey(25)
                # # Send frame to client
                # _, buffer = cv2.imencode('.jpg', frame)
                # data = buffer.tobytes()
                # client_socket.sendall(data)

            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message == "Pause":
                cv2.waitKey(-1) # wait until any key is pressed
                paused = True
            elif message == "Play":
                key = ord('r')
                paused = False
            elif message == "Quit":
                break

        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()

        server_socket.close()

if __name__ == "__main__":
    video_path = 'sample-media/sample-vid-3.mp4'
    start_end_device_server(video_path)
