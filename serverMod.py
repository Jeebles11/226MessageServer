#!/usr/bin/python3
import socket
#import sys


def send_reply(reply):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination
    


BUF_SIZE = 1024
#HOST = ''
HOST = '10.21.75.90'
PORT = 12299
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
    print(fullS + " is the recieved string")
    goodKey = False
    goodMessage = False


    if len(fullS) < 13: #a valid message will have 13chars before the message starts.
        reply = ("No, command and key too short \n").encode('utf-8')
        send_reply(reply)
        command = "bad"
    else:
        command = fullS[0:3]
    try:   
        if command == "PUT" or command == "put":
            messageKey = fullS[4 :12]
            if (messageKey.isalnum() == False):
                reply = ("NO! Please use only alphanum chars for key.\n").encode('utf-8')
                send_reply(reply) 
            else:
                goodKey = True

            savedMessage = fullS[13:-1] #a valid message will have 13chars before the message starts.
            if len(savedMessage) > 160: #if user enters a message longer than 160 bytes in length, truncates
                savedMessage = savedMessage[0: 160]
                reply = ("No, message too long\n").encode('utf-8')
                send_reply(reply)

            elif len(savedMessage) == 0:
                reply = ("No, message empty\n").encode('utf-8')
                send_reply(reply)

            elif savedMessage.isspace() == True:
                reply = ("No, message is only whitespace\n").encode('utf-8')
                send_reply(reply)

            else:
                goodMessage = True

            print(messageKey + " is the message key")
            print(savedMessage + " is the saved message")

            if goodKey and goodMessage:
                messageDict = { messageKey : savedMessage}
                print(messageDict)
                reply = ("Okay \n").encode('utf-8')
                send_reply(reply)
        
        elif command == "GET" or command == "get":
            messageToReturnKey = fullS[4 :12]
            if messageDict == None:
                reply = ("No saved keys. \n").encode('utf-8')
                send_reply(reply)

            else:
                try:
                    messageToReturn = messageDict[messageToReturnKey]
                    reply = (messageToReturn + "\n").encode('utf-8')
                except:
                    print("not a valid key") 
                    reply = ("\n").encode('utf-8')
                finally:
                    send_reply(reply)


        else:
            reply = ("NO! Please use put or get command.\n").encode('utf-8')
            send_reply(reply)
        #reply = ("Recieved: " + fullS).encode('utf-8')
    except:
        print("Something went wrong.")
    


