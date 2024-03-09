# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)