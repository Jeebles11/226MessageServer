#!/usr/bin/python3
import asyncio
import sys
import random 
import traceback
import string


CMD_LENGTH = 3
KEY_LENGTH = 8
MESSAGE_EXISTS = "NO "
PUT_CMD = "PUT"
GET_CMD = "GET"
SERVER_HOST = sys.argv[1]
SERVER_PORT = sys.argv[2]
PING_IN_SECONDS = 5

currentKey = ""  #GLOBAL !!

#takes no params, generates a random key for the next message in the linked list
# get random key of length KEY_LENGTH ( 8 ) with letters(upperCase & lowercase) + digits
def generateKey():
    characters = string.ascii_letters + string.digits
    randomKey = ''.join(random.choice(characters) for i in range(KEY_LENGTH)) #plus one to ensure we get the full 8 chars
    #print("Random password is:", randomKey)
    return randomKey


#takes the string entered by user as the param
# calls upon generateKey to create a Key of KEY_LENGTH chars (8), then concats it with the orig key and usr provided string. 
# This message is then returned, and sent by startConnection.    
def generateMessageToServer(usrString):
    global currentKey
    randomKey = generateKey()
    return((PUT_CMD + currentKey + randomKey + usrString + "\n").encode('utf-8')) #first KEY_LENGTH (8) bytes of message is the "nextKey"


#Takes in the message (already encoded) as a Param
#Creates one instance of a socket connection to read in a message, and then send a message. 
#Also prints the recieved messages to console. 
async def startConnection(message_to_send):
    global currentKey
    reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
    writer.write(message_to_send)
    data = await reader.readline()
    writer.close() # wait until the sever response comes through before closing the connection (the read function)
    await writer.wait_closed() # wait until writer completes close()
    decodedData = data.decode("utf-8")
    print(f'Received: {decodedData[(CMD_LENGTH + KEY_LENGTH) : ]}') #after char 11 (as of time of writing), the user provided message begins 
    return decodedData


#takes in no params
#is responsible for repeatadly pinging the server looking for new messages at the current key 
#if a user connects, and there are already messages at that dictionary key, displays all messages currently in the thread
#purposfully in an infinate loop to search for new messages until user disconnects 
async def recieveMessage():
    global currentKey
    while True:
        decodedData = await startConnection(( GET_CMD + currentKey + '\n').encode('utf-8'))

        while(decodedData [ : CMD_LENGTH] == MESSAGE_EXISTS):         #if NO message was recieved, that means there is a message at that key! 
            currentKey = decodedData[CMD_LENGTH : (CMD_LENGTH + KEY_LENGTH) ] #gets key located after the NO message that is KEY_LENGTH (8) long. If we changed the message then this shouldn't break 
            decodedData = await startConnection(( GET_CMD + currentKey + '\n').encode('utf-8'))
            
        await asyncio.sleep(PING_IN_SECONDS)
        #print("I waited 5 seconds")
        

#prompts the user to input a message. Does NOT block the thread while waiting for input! 
# If a message already exists at the current key, continues to loop through the linked list until the key with no message is found, and saves the message at that key.   
async def writeMessage():
    while True:
        global currentKey
        loop = asyncio.get_running_loop()

        nextMessage = await loop.run_in_executor(None, input, "> ") #this is our fancy way to get input that doesn't block the thread (unlike the regular input() function)
        toSend = generateMessageToServer(nextMessage) #toSend is already encoded
        decodedData = await startConnection(toSend)


        while(decodedData [ : CMD_LENGTH] == MESSAGE_EXISTS):         #if NO message was recieved, that means there is a message at that key! 
            currentKey = decodedData[3 : 11]
            toSend = generateMessageToServer(nextMessage)
            decodedData = await startConnection(toSend)
        
    

#this function is the 'main' runner of the program. 
#takes in no params, however gets vars off the command line using sys.argv. 
#exceptions could be thrown (without the try catch), if usr inputs invalid input.

#if there is no messages for a user provided key, starts a new message 'thread' (think reddit thread, not a multithreading thread)
#the message thread is implemented with a link list of keys. Each message containing the pointer to the next message in the first KEY_LENGTH (8) chars of the message
#if there is messages in the thread, continue printing messages until reaching a newline(empty node), then prompt usr for next message
#the server connection appears to the user to never terminate; instead pings the server continiously looking for new messages. 
async def client():
    global currentKey
    try:
        currentKey = sys.argv[3]
        await asyncio.gather(recieveMessage(), writeMessage())

    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass

    sys.exit(-1)

asyncio.run(client())
