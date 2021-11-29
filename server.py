#!/usr/bin/python3   #lock should happen JUST as you access the dictionary- 
import traceback
import asyncio

CMD_LENGTH = 3
MESSAGE_MAX = 11
PUT_CMD = "PUT"
GET_CMD = "GET"
BAD_PUT_REPLY = "NO\n"
BAD_GET_REPLY = "\n"
GOOD_PUT_REPLY = "OK\n"
MAX_MESSAGE_BYTES = 160
BUF_SIZE = 1024
HOST = '::1'
PORT = 12345

messageDict = {} #global message dictionary

#this function takes the reply generated from the program, and sends it over to the client via TCP.
#the param reply is either NO (used in put command) or \n (used in get command). Sends OK if PUT command was succesful,
#OR the retrieved message if the GET commmand was succesful
#Params: the generated reply, and the client where the response will go 
async def send_reply(reply, writer):
    writer.write(reply) # starts to write the data to the stream
    await writer.drain() # waits until the data is written
    writer.close()
    await writer.wait_closed()

#this function returns the KEY for locating the message.
#no changes are made to the orig string.   
#param fullS is the entire decoded string sent from client. 
def get_message_key_from_fullString(fullS):
    return fullS[CMD_LENGTH : MESSAGE_MAX]

#this function handles checking various scenarios within the command 'PUT'
#exits the function by sending NO if standards are not met
#If all standards ARE met, the semaphore locks access to the dictonary while the thread writes in a new entry.
#params: fullS is the entire decoded string sent from client, client is the active client(thread)
async def put_command(fullS, writer):
    global messageDict
    reply = (BAD_PUT_REPLY).encode('utf-8')
    messageKey = get_message_key_from_fullString(fullS)

    
    
    if (len(fullS) < MESSAGE_MAX ) or (messageKey.isalnum() == False): 
        #reply = ("No, command and key too short \n").encode('utf-8')
        await send_reply(reply, writer)
        
    else:
        savedMessage = fullS[MESSAGE_MAX : ]
        
        if (len(savedMessage) > MAX_MESSAGE_BYTES) or (len(savedMessage) == 0) or (savedMessage.isspace() == True): 
            #if message too long, message empty, or only whitespace, reject
            await send_reply(reply, writer)
        
        # elif len(messageDict [messageKey]) > 2:
        #     print("MESSAGE ALREDY EXISTS FOR THIS KEY!!!!")
        #     await send_reply("mesE".encode('utf-8'), writer)
        else: 
            try:
                DATA = messageDict [messageKey]

            except:                                      #if we get an exception, that means we ARE allowed to install a new message in the dict (cuz it's empty)
                messageDict [messageKey] = savedMessage
                reply = (GOOD_PUT_REPLY).encode('utf-8')
                await send_reply(reply, writer)
                return

            
            currentMessage = messageDict[messageKey].encode('utf-8')
            print("MESSAGE ALREDY EXISTS FOR THIS KEY!!!!")
            await send_reply(("NO " + messageDict[messageKey]).encode('utf-8'), writer)
        
    #print(messageDict[messageKey]   + "  is dict check")
        ########## END PUT COMMAND ##########

#this function handles checking various scenarios within the command 'GET'. ensures key is valid before access
#exits the function by sending \n if standards are not met    
#the semaphore locks the dict while accessing the data from a valid key
#params: fullS is the entire decoded string sent from client, client is the active client(thread)
async def get_command(fullS, writer):
    reply = (BAD_GET_REPLY).encode('utf-8')
    messageToReturnKey = get_message_key_from_fullString(fullS)
    
    if messageDict == None:
        await send_reply(reply, writer)
    else:
        try:
            messageToReturn = messageDict[messageToReturnKey]
            #print(messageToReturn + " is the mess to return ")
            reply = ("NO " + messageToReturn + '\n').encode('utf-8') 
        except Exception:
            pass
        finally:
            await send_reply(reply, writer)
########## END GET COMMAND ##########



#this function runs off the newly made thread, and is responsible for reading in data and managing the commands
#asyncio reader and writer co routine is started in main(), and passes in writer and reader to this function
# Only TWO vaild commands (for now ) PUT & GET 
#any exceptions thrown will print details to the server command line 
async def start_connect(reader, writer):
    data = await reader.readline()
    fullS = data.decode('utf-8').strip()
    #print(fullS + " recieved from client")
    command = fullS[0:CMD_LENGTH]

    try:
        ########## START PUT COMMAND ##########   
        if command == PUT_CMD:
            await put_command(fullS, writer)

        ########## START GET COMMAND ##########
        elif command == GET_CMD:
            await get_command(fullS, writer)
        ##########if you wanted to add more commands, they go here ###########
        else:
            #you put something weird, reject
            reply = (BAD_PUT_REPLY).encode('utf-8')
            await send_reply(reply, writer)
        
    except Exception as details:
                    print(details)
                    traceback.print_exc()
                    pass


async def main():
    server = await asyncio.start_server(start_connect, HOST, PORT)
    await server.serve_forever() # without this, program terminates


asyncio.run(main())

    