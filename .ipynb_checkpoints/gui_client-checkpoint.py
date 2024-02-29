import socket

def run_gui_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = 'remote_server_ip'
    server_port = 12345
    client_socket.connect((server_ip, server_port))
    data_to_send = "Hello from GUI client"
    client_socket.sendall(data_to_send.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print("Response from server:", response)
    client_socket.close()

if __name__ == "__main__":
    run_gui_client()
