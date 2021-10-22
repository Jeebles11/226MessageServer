#!/usr/bin/python3
import asyncio
import sys
import random 
import traceback

SERVER_HOST = sys.argv[1]
SERVER_PORT = sys.argv[2]
async def promptForMessage(message_key):
    randomKey = random.randint(12345070, 12345680)        #smaller range for testing
    #randomKey = random.randint(10000000, 99999999)          #could potentially cause a collision ? use alphanum
    randomKey = str(randomKey)

    reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
    print("Enter a message for key "+ message_key + "\n")
    messageToSend = "PUT"+ message_key + randomKey + input() + "\n" #first 8 bytes of message is the "nextKey"
    messageToSend = messageToSend.encode()
    #print(str(messageToSend) + " is the message to send")
    
    #writer.write((messageToSend).encode('utf-8') + b'\n')
    writer.write(messageToSend)
    data = await reader.readline() # more on this on the next slides
    print(f'Received: {data.decode("utf-8")}')

    await writer.drain()
    writer.close() # reader has no close() function
    await writer.wait_closed() # wait until writer completes close()

async def recieveMessage(reader):
    print()

async def client():
    try:
        if (True):
            reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
            message_key = sys.argv[3]
            print(sys.argv[1], sys.argv[2], sys.argv[3])
            writer.write(("GET"+sys.argv[3]).encode('utf-8') + b'\n')
            await writer.drain()
            data = await reader.readline() # more on this on the next slides
            print(f'Received: {data.decode("utf-8")}')
            
            while(len(data) > 2):
                readerr, writerr = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
                message_key = (data[ : 8]).decode("utf-8")
                writerr.write(("GET"+message_key).encode('utf-8') + b'\n')
                data = await readerr.readline()
                print(f'Received: {data.decode("utf-8")}')

            
            
            await promptForMessage(message_key)

    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass

    sys.exit(-1)

asyncio.run(client())
