#!/usr/bin/python3
import socket
import sys
import struct 
import threading

BUF_SIZE = 4096
HOST = ''
PORT = 12345
locks = []


def get_line(client):
    buffer = b''
    size = 0
    while True:
        data = client.recv(1)
        size += 1
        if data == b'\n' or size >= BUF_SIZE:
                return buffer
        buffer = buffer + data

def start_connect(thread_id, client):
    #print('Client:', client.getpeername()) # Destination IP and port

    data = get_line(client)

    locks[thread_id].release()
    print(data.decode())
    locks[thread_id].acquire()






sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen() # Enable server to receive 1 connection at a time

numClients = 0
while True:
    #print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established

    #after sock accept, create new thread, all work done there
    threading.Thread(target = start_connect, args = (i, client)).start()
    numClients = numClients + 1
    locks.append(threading.Semaphore())
    locks[-1].acquire()