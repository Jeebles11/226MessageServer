#!/usr/bin/python3
import socket
import struct 

def readIn(s,c): #s is socket, c is STOP CHAR, n is n times the stop char must appear to stop read
    data = s.recv(1)
    n = c.struct.unpack('!B', data)
    charCount =0
    buffer = b"
    while charCount < n:
        data = s.recv(1)
        if data = c: 
            charCount = Charcount + 1
        buffer = buffer + data

    return buffer


BUF_SIZE = 1024
HOST = ''
#HOST = '10.21.75.90'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen() # Enable server to receive 1 connection at a time
messageDict = None

while True:
    print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established
    print('Client:', client.getpeername()) # Destination IP and port
    data = readIn(sock, '*')
