#!/usr/bin/python3
import asyncio
import sys
import random 
import traceback
import string

SERVER_HOST = sys.argv[1]
SERVER_PORT = sys.argv[2]
KEY_LENGTH = 8

#takes no params, generates a random key for the next message in the linked list
# get random key of length KEY_LENGTH ( 8 ) with letters(upperCase & lowercase) + digits
def generateKey():
    characters = string.ascii_letters + string.digits
    randomKey = ''.join(random.choice(characters) for i in range(KEY_LENGTH + 1)) #plus one to ensure we get the full 8 chars
    #print("Random password is:", randomKey)

    return randomKey

#this function takes in the empty node in the linked list, and prompts user to enter another message
#I split this function and generateMessageToServer into two seperate functions to adhere to the rule that "a function should do just one thing",
#  Let me know if that is the right idea in this situation :)
#I left this function as await, because usr could be slow writing the input. is this right?
async def promptForMessage(message_key):
    print("Please enter a new message: \n")
    usrString = input()

    return usrString
    
def generateMessageToServer(message_key, usrString):
    randomKey = generateKey()
    return(("PUT"+ message_key + randomKey + usrString + "\n").encode('utf-8')) #first KEY_LENGTH (8) bytes of message is the "nextKey"



async def recieveMessage(reader):
    data = await reader.readline()
    decodedData = data.decode("utf-8")
    print(f'Received: {decodedData[9 : ]}')
    return data
    
async def writeMessage(toSend, writer):
    #print(str(toSend) + " is the message about to send")
    writer.write(toSend)
    
    
async def createConnection(messageToSend):
    reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
    await writeMessage(messageToSend, writer)

    data = await recieveMessage(reader)

    await writer.drain()
    writer.close() # wait until the sever response comes through before closing the connection (the read function)
    await writer.wait_closed() # wait until writer completes close()
    return data

async def client():
    try:
        message_key = sys.argv[3]
        
        data = await createConnection(( "GET"+ message_key + '\n').encode('utf-8'))  #any way I can not repeat myself here?

        while(len(data) > 2):
            message_key = (data[ : KEY_LENGTH]).decode("utf-8")
            data = await createConnection(( "GET"+ message_key + '\n').encode('utf-8'))

        newUsrMessage = await promptForMessage(message_key)
        await createConnection(generateMessageToServer(message_key, newUsrMessage)) #createConnection returns 'Data', but since it's just the put message, we don't need to do anything with it

    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass

    sys.exit(-1)

asyncio.run(client())
