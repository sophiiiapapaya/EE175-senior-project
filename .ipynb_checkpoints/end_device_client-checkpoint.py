# end_device_client.py
import socket

def end_device_hostname():
    hostname = socket.gethostname()
    return hostname

# def connect_to_gui_client():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     hostname = end_device_hostname()

#     try:
#         server_ip = socket.gethostbyname(hostname)
#         print(f'The {hostname} IP Address is {server_ip}')
#     except socket.gaierror as e:
#         print(f'Invalid hostname, error raised is {e}')
#         return
    
#     server_port = 12345
#     client_socket.connect((server_ip, server_port))
#     data_to_send = "Hello from end device"
#     client_socket.sendall(data_to_send.encode('utf-8'))
#     response = client_socket.recv(1024).decode('utf-8')
#     print("Response from server:", response)
#     client_socket.close()

def start_end_device_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # hostname = end_device_hostname()
    # server_ip = socket.gethostbyname(hostname)
    server_ip = '0.0.0.0' # All availabe interfaces
    
    server_port = 12345  # Choose a different port for the server
    
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for one incoming connection
    
    print(f"End device server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to GUI client:', addr)
    
        while True:
            # Receive data from GUI client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("Received from GUI client:", data)
                    
            # Send response back to GUI client
            response = "Message received by end device"
            client_socket.sendall(response.encode('utf-8'))
        
        client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_end_device_server()
    # connect_to_gui_client()
