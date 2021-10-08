#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import socket
CMD_LENGTH = 3
MESSAGE_MAX = 11
PUT_CMD = "PUT"
GET_CMD = "GET"
messageDict = None #global message dictionary

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply defaults to either NO (put command) or \n (get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
def send_reply(reply):
    client.sendall(reply) # Destination IP and port implicit due to accept call
    client.close() # Termination

#this function returns the KEY for locating the message. Takes no params as fullS is a global variable (uh oh)
#no changes are made to the orig string.    
def get_message_key_from_fullString():
    return fullS[CMD_LENGTH : MESSAGE_MAX]

def put_command():
    reply = ("NO\n").encode('utf-8')
    print("in the method")
    messageKey = get_message_key_from_fullString()
    print(str(len(fullS)))
    if len(fullS) < MESSAGE_MAX: #a valid message will have 12chars before the message starts.
        #reply = ("No, command and key too short \n").encode('utf-8')
        send_reply(reply)
        print("in the 1")
    elif (messageKey.isalnum() == False):
        #reply = ("NO! Please use only alphanum chars for key.\n").encode('utf-8')
        send_reply(reply) 
        print("in the 2")
    else:
        savedMessage = fullS[MESSAGE_MAX:-1] #a valid message will have 12chars before the message starts.
        print("in the 3")
        
    maxMessageInBytes = 160
    if len(savedMessage) > maxMessageInBytes: #if user enters a message longer than 160 bytes in length, rejects 
        #reply = ("No, message too long\n").encode('utf-8')
        send_reply(reply)
        print("in the 4")

    elif len(savedMessage) == 0:
        #reply = ("No, message empty\n").encode('utf-8')
        send_reply(reply)
        print("in the 5")

    elif savedMessage.isspace() == True:
        #reply = ("No, message is only whitespace\n").encode('utf-8')
        send_reply(reply)
        print("in the 6")

    else:
        global messageDict 
        messageDict = { messageKey : savedMessage}
        reply = ("OK\n").encode('utf-8')
        send_reply(reply)
        print(messageDict)

        ########## END PUT COMMAND ##########

    
def get_command():
    reply = ("\n").encode('utf-8')
    messageToReturnKey = get_message_key_from_fullString()
    print(messageDict)
    if messageDict == None:
        send_reply(reply)
        print("in the none")
    else:
        try:
            messageToReturn = messageDict[messageToReturnKey]
            reply = (messageToReturn + "\n").encode('utf-8')
            print("in the try")
        except Exception:
            pass
        finally:
            send_reply(reply)
########## END GET COMMAND ##########

BUF_SIZE = 1024
HOST = ''
#HOST = '10.21.75.90'
PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen() # Enable server to receive 1 connection at a time


while True:
    print("Waiting to recieve message from client.")
    client, sockname = sock.accept() # Wait until a connection is established
    print('Client:', client.getpeername()) # Destination IP and port
    data = client.recv(BUF_SIZE) # recvfrom not needed since address is known
    #FIXME: recive should continue to recive until a newline is reached. While loop?
    fullS = data.decode()
    
    
    command = fullS[0:CMD_LENGTH]
    try:
        ########## START PUT COMMAND ##########   
        if command == PUT_CMD:
            put_command()

        ########## START GET COMMAND ##########
        elif command == GET_CMD:
            get_command()

        else:
            reply = ("NO\n").encode('utf-8')
            send_reply(reply)
        
    except Exception as details:
                    print(details)
                    pass