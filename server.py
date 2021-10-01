#!/usr/bin/python3
import socket

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply defaults to either NO (put command) or \n (get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
def send_reply(reply):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination

#this function returns the KEY for locating the message. Takes no params as fullS is a global variable (uh oh)
#no changes are made to the orig string.    
def get_message_key_from_fullString():
    return fullS[3 :11]

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
    data = client.recv(BUF_SIZE) # recvfrom not needed since address is known
    fullS = data.decode()
    
    reply = ("NO\n").encode('utf-8')
    command = fullS[0:3]
    try:
        ########## START PUT COMMAND ##########   
        if command == "PUT" or command == "put":
            messageMax = 11

            messageKey = get_message_key_from_fullString()
            if (messageKey.isalnum() == False):
                #reply = ("NO! Please use only alphanum chars for key.\n").encode('utf-8')
                send_reply(reply) 
            elif len(fullS) < messageMax: #a valid message will have 12chars before the message starts.
                #reply = ("No, command and key too short \n").encode('utf-8')
                send_reply(reply)
                #command = "bad"
            else:
                savedMessage = fullS[messageMax:-1] #a valid message will have 12chars before the message starts.

            

            maxMessageInBytes = 160
            if len(savedMessage) > maxMessageInBytes: #if user enters a message longer than 160 bytes in length, rejects 
                #reply = ("No, message too long\n").encode('utf-8')
                send_reply(reply)

            elif len(savedMessage) == 0:
                #reply = ("No, message empty\n").encode('utf-8')
                send_reply(reply)

            elif savedMessage.isspace() == True:
                #reply = ("No, message is only whitespace\n").encode('utf-8')
                send_reply(reply)

            else:
                messageDict = { messageKey : savedMessage}
                reply = ("OK\n").encode('utf-8')
                send_reply(reply)

        ########## END PUT COMMAND ##########

        ########## START GET COMMAND ##########
        elif command == "GET" or command == "get":
            reply = ("\n").encode('utf-8')
            messageToReturnKey = get_message_key_from_fullString()

            if messageDict == None:
                send_reply(reply)

            else:
                try:
                    messageToReturn = messageDict[messageToReturnKey]
                    reply = (messageToReturn + "\n").encode('utf-8')
                except Exception:
                    pass
                finally:
                    send_reply(reply)
        ########## END GET COMMAND ##########

        else:
            send_reply(reply)
        
    except Exception:
                    pass