#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import socket
import threading
import time
import traceback

CMD_LENGTH = 3
MESSAGE_MAX = 11
PUT_CMD = "PUT"
GET_CMD = "GET"
MAX_MESSAGE_BYTES = 160
messageDict = {} #global message dictionary

BUF_SIZE = 1024
HOST = ''
#HOST = '10.21.75.90'
PORT = 12345

locks = []
locks.append(threading.Semaphore()) #add the semaphore to lock array

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply defaults to either NO (put command) or \n (get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
#FIXME: SOME HOW CLIENT NEEDS TO GO IN THERE
def send_reply(reply, client):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination

#this function returns the KEY for locating the message. Takes no params as fullS is a global variable (uh oh)
#no changes are made to the orig string.    
def get_message_key_from_fullString(fullS):
    return fullS[CMD_LENGTH : MESSAGE_MAX]

def put_command(fullS, client):
    reply = ("NO\n").encode('utf-8')
    
    messageKey = get_message_key_from_fullString(fullS)
    
    if len(fullS) < MESSAGE_MAX: #a valid message will have 12chars before the message starts.
        #reply = ("No, command and key too short \n").encode('utf-8')
        send_reply(reply, client)
        
    elif (messageKey.isalnum() == False):
        #reply = ("NO! Please use only alphanum chars for key.\n").encode('utf-8')
        send_reply(reply, client) 
        
    else:
        savedMessage = fullS[MESSAGE_MAX : ] #a valid message will have 12chars before the message starts.
        

    if len(savedMessage) > MAX_MESSAGE_BYTES: #if user enters a message longer than 160 bytes in length, rejects 
        #reply = ("No, message too long\n").encode('utf-8')
        send_reply(reply, client)

    elif len(savedMessage) == 0:
        #reply = ("No, message empty\n").encode('utf-8')
        send_reply(reply, client)
    
    elif savedMessage.isspace() == True:
        #reply = ("No, message is only whitespace\n").encode('utf-8')
        send_reply(reply, client)
        
    else:
        locks[0].acquire()
        global messageDict 
        messageDict [messageKey] = savedMessage
        locks[0].release()
        reply = ("OK\n").encode('utf-8')
        send_reply(reply, client)
        
        ########## END PUT COMMAND ##########

    
def get_command(fullS, client):
    reply = ("\n").encode('utf-8')
    messageToReturnKey = get_message_key_from_fullString(fullS)
    
    if messageDict == None:
        send_reply(reply, client)
        print("in the none")
    else:
        try:
            locks[0].acquire()
            messageToReturn = messageDict[messageToReturnKey]
            reply = (messageToReturn + "\n").encode('utf-8')
            print("in the try")
        except Exception:
            pass
        finally:
            locks[0].release()
            send_reply(reply, client)
########## END GET COMMAND ##########

def get_line(client):
    buffer = b''
    size = 0
    while True:
        data = client.recv(1)
        #print(str(data))
        size += 1
        if data == b'\n' or size >= BUF_SIZE:
                print(str(buffer))
                return buffer
        buffer = buffer + data


def start_connect(thread_id, client):
    print('Client:', client.getpeername()) # Destination IP and port

    data = get_line(client)
        
    
    fullS = data.decode()
    print(fullS + " is after the decode")
    
    command = fullS[0:CMD_LENGTH]
    try:
        ########## START PUT COMMAND ##########   
        if command == PUT_CMD:
            put_command(fullS, client)

        ########## START GET COMMAND ##########
        elif command == GET_CMD:
            get_command(fullS, client)

        else:
            reply = ("NO\n").encode('utf-8')
            send_reply(reply, client)
        
    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen() # Enable server to receive 1 connection at a time

i = 0
while True:
    print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established
    #after accept, create new thread? do everything there
    threading.Thread(target = start_connect, args = (i, client)).start()
    i = i + 1
    