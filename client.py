#!/usr/bin/python3
import socket
import sys
BUF_SIZE = 1024
HOST = '192.168.0.153'
PORT = 65432
if len(sys.argv) != 2:
print(sys.argv[0] + ' <message>')
sys.exit()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.connect((HOST, PORT)) # Initiates 3-way handshake
print('Client:', sock.getsockname()) # Source IP and source port
data = sys.argv[1].encode('utf-8')
sock.sendall(data) # Destination IP and port implicit due to connect call
reply = sock.recv(BUF_SIZE) # recvfrom not needed since address is known
print('Reply:', reply)
sock.close() # Termination
37