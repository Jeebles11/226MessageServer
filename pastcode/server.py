#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import socket
import threading
import time
import traceback

CMD_LENGTH = 3
MESSAGE_MAX = 11
PUT_CMD = "PUT"
GET_CMD = "GET"
BAD_PUT_REPLY = "NO\n"
BAD_GET_REPLY = "\n"
GOOD_PUT_REPLY = "OK\n"
MAX_MESSAGE_BYTES = 160
BUF_SIZE = 1024
HOST = ''
PORT = 12333

messageDict = {} #global message dictionary
locks = [] #for this purpose we don't really require an array, but will keep it so in the future, we can add more semaphores if we need. 
locks.append(threading.Semaphore()) #add the semaphore to lock array

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply is either NO (used in put command) or \n (used in get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
#Params: the generated reply, and the client where the response will go 
def send_reply(reply, client):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination

#this function returns the KEY for locating the message.
#no changes are made to the orig string.   
#param fullS is the entire decoded string sent from client. 
def get_message_key_from_fullString(fullS):
    return fullS[CMD_LENGTH : MESSAGE_MAX]

#this function handles checking various scenarios within the command 'PUT'
#exits the function by sending NO if standards are not met
#If all standards ARE met, the semaphore locks access to the dictonary while the thread writes in a new entry.
#params: fullS is the entire decoded string sent from client, client is the active client(thread)
def put_command(fullS, client):
    reply = (BAD_PUT_REPLY).encode('utf-8')
    messageKey = get_message_key_from_fullString(fullS)
    
    if len(fullS) < MESSAGE_MAX: 
        #reply = ("No, command and key too short \n").encode('utf-8')
        send_reply(reply, client)
        
    elif (messageKey.isalnum() == False):
        #reply = ("NO! Please use only alphanum chars for key.\n").encode('utf-8')
        send_reply(reply, client) 
        
    else:
        savedMessage = fullS[MESSAGE_MAX : ]
        
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
        reply = (GOOD_PUT_REPLY).encode('utf-8')
        send_reply(reply, client)
        
        ########## END PUT COMMAND ##########

#this function handles checking various scenarios within the command 'GET'. ensures key is valid before access
#exits the function by sending \n if standards are not met    
#the semaphore locks the dict while accessing the data from a valid key
#params: fullS is the entire decoded string sent from client, client is the active client(thread)
def get_command(fullS, client):
    reply = (BAD_PUT_REPLY).encode('utf-8')
    messageToReturnKey = get_message_key_from_fullString(fullS)
    
    if messageDict == None:
        send_reply(reply, client)
    else:
        try:
            locks[0].acquire()
            messageToReturn = messageDict[messageToReturnKey]
            reply = (messageToReturn + "\n").encode('utf-8')
        except Exception:
            pass
        finally:
            locks[0].release()
            send_reply(reply, client)
########## END GET COMMAND ##########

#reads in data until either a newline is found, or buffer sized is reached
#PARAMS: the active client (thread) is passed in. 
def get_line(client):
    buffer = b''
    size = 0
    while True:
        data = client.recv(1)
        size += 1
        if data == b'\n' or size >= BUF_SIZE:
                return buffer
        buffer = buffer + data

#this function runs off the newly made thread, and is responsible for reading in data and managing the commands
#main 'workhorse' function 
#any exceptions thrown will print details to the server command line 
def start_connect(thread_id, client):
    #print('Client:', client.getpeername()) # Destination IP and port

    data = get_line(client)
    fullS = data.decode()
    command = fullS[0:CMD_LENGTH]

    try:
        ########## START PUT COMMAND ##########   
        if command == PUT_CMD:
            put_command(fullS, client)

        ########## START GET COMMAND ##########
        elif command == GET_CMD:
            get_command(fullS, client)

        else:
            reply = (BAD_PUT_REPLY).encode('utf-8')
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
    #print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established

    #after sock accept, create new thread, all work done there
    threading.Thread(target = start_connect, args = (i, client)).start()
    i = i + 1
    