# client.py -- send frame
import socket
import cv2

def play_video(video_path, server_address, server_port):
    cap = cv2.VideoCapture(video_path)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    client_socket.sendall(video_path.encode('utf-8'))
    paused = False

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Video sending', frame)

        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            message = "Quit"
            client_socket.sendall(message.encode('utf-8'))
            break
        elif key == ord('p'):  # Pause or resume the video
            if paused:
                paused = False
                message = "Play"
            else:
                paused = True
                message = "Pause"
                cv2.waitKey(-1) # wait until any key is pressed
                if key == ord('p'):  # Pause or resume the video
                    paused = False
                    message = "Play"
            client_socket.sendall(message.encode('utf-8'))

        # Send message to server
        message = "Playing video"
        client_socket.sendall(message.encode('utf-8'))

    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()

if __name__ == "__main__":
    video_path = 'sample-media/sample-vid-3.mp4'
    server_address = '127.0.0.1'  # Change this to your server's IP address
    server_port = 12345  # Change this to your server's port number
    play_video(video_path, server_address, server_port)
