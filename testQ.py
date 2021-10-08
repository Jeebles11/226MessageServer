#!/usr/bin/python3
import socket
import struct

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply defaults to either NO (put command) or \n (get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
def send_reply(reply):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination

def theSocket(usrPortNumber):
    BUF_SIZE = 1024
    HOST = ''
    #HOST = '10.21.75.90'
    PORT = usrPortNumber
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Enable server to receive 1 connection at a time
    

    while True:
        number = struct.unpack('!h', sock.recv(2))[0]
        if number == -1:
            break
        theArray.append(number)






    return numbers





theSocket(12345)