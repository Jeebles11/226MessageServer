#!/usr/bin/python3
import asyncio
import sys
import random 
import traceback

SERVER_HOST = sys.argv[1]
SERVER_PORT = sys.argv[2]
KEY_LENGTH = 8

def generateKey():
    randomKey = random.randint(12345070, 12345680)        #smaller range for testing FIXME: DO ALPHANUM KEY!
    #randomKey = random.randint(10000000, 99999999)          #could potentially cause a collision ? use alphanum
    return randomKey

async def promptForMessage(message_key):
    randomKey = generateKey()
    
    randomKey = str(randomKey)

    print("Enter a message for key "+ message_key + "\n")
    messageToSend = ("PUT"+ message_key + randomKey + input() + "\n").encode('utf-8') #first KEY_LENGTH (8) bytes of message is the "nextKey"

    return messageToSend
    

async def recieveMessage(reader):
    data = await reader.readline()
    #print(str(data) + " is the data in recMessage")
    print(f'Received: {data.decode("utf-8")}')
    return data
    
async def writeMessage(toSend, writer):
    print(str(toSend) + " is the message about to send")
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

        newMessage = await promptForMessage(message_key)
        await createConnection(newMessage) #createConnection returns 'Data', but since it's just the put message, we don't need to do anything with it

    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass

    sys.exit(-1)

asyncio.run(client())
