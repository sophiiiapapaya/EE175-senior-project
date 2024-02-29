import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server's IP address and port
server_ip = '0.0.0.0'  # Use 0.0.0.0 to listen on all available interfaces
server_port = 12345

# Bind to the IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)

print("Server listening on {}:{}".format(server_ip, server_port))

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    print("Received from client:", data)

    # Echo the received data back to the client
    client_socket.sendall(data.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()
