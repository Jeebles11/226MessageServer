#!/usr/bin/python3
import socket
import sys

BUF_SIZE = 160
#HOST = ''
HOST = '10.21.75.90'
PORT = 12311
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen() # Enable server to receive 1 connection at a time
while True:
    print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established
    print('Client:', client.getpeername()) # Destination IP and port
    data = client.recv(BUF_SIZE) # recvfrom not needed since address is known
    s = data.decode()
    print(s)
    reply = ("Recieved: " + s).encode('utf-8')
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination
    sys.exit()


