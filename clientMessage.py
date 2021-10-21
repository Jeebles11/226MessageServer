#!/usr/bin/python3
import socket
import sys
import struct 
BUF_SIZE = 1024
HOST = ''
PORT = 12333

#  len(sys.argv) != 1:
#     print(sys.argv[0] + ' <message>')
#     sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.connect((HOST, PORT)) # Initiates 3-way handshake
print('Client:', sock.getsockname()) # Source IP and source port

while (True):
    print("what is ur message")
    mess = input()
    sock.sendall(mess.encode('utf-8')) # Destination IP and port implicit due to connect call
    reply = sock.recv(BUF_SIZE) # recvfrom not needed since address is known
    print('Reply:', reply)
    sock.close() # Termination
