#!/usr/bin/python3
import socket
import sys
import struct 
BUF_SIZE = 1024
HOST = ''
PORT = 12345

# if len(sys.argv) != 1:
#     print(sys.argv[0] + ' <message>')
#     sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.connect((HOST, PORT)) # Initiates 3-way handshake
print('Client:', sock.getsockname()) # Source IP and source port
print("what is ur guess 1-100")
num = b''
num = num +  int(input())
data = struct.pack('!B', num)
sock.sendall(data) # Destination IP and port implicit due to connect call
reply = sock.recv(BUF_SIZE) # recvfrom not needed since address is known
print('Reply:', reply)
sock.close() # Termination
