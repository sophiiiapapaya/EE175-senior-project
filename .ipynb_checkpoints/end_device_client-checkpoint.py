# end_device_client.py
import socket

def end_device_hostname():
    hostname = socket.gethostname()
    return hostname

def connect_to_gui_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # char localhostname[255];
    hostname = end_device_hostname()
    # gui_client.get_ip_address(hostname) # pass the hostname to gui_client.py

    try:
        server_ip = socket.gethostbyname(hostname)
        print(f'The {hostname} IP Address is {server_ip}')
    except socket.gaierror as e:
        print(f'Invalid hostname, error raised is {e}')
        
    server_port = 12345
    client_socket.connect((server_ip, server_port))
    data_to_send = "Hello from end device"
    client_socket.sendall(data_to_send.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print("Response from server:", response)
    client_socket.close()

if __name__ == "__main__":
    connect_to_gui_client()
