import socket
import sys
import os

#PART 0 : CONNECT
HOST = sys.argv[1]  # The server's hostname or IP address
PORT = int(sys.argv[2])        # The port used by the server
debugMode =  True if sys.argv[3] == '1' else False 
c = 0

#PART 1 : SEND COMMAND
while True:      
    buffer = bytearray()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))  
    if(c==0):
        print("Session has been established.")
        c+=1
    command = input('myftp> ')
    commandList = command.split(' ')
    opcode = commandList[0]
    
    if (opcode == "help"):
        Opcode = (3 & 0b111) << 5
        buffer.append(Opcode)        
    #put
    elif(opcode=='put'):
        #geting the upcode
        Opcode = (0 & 0b111) << 5
        #geting the file length
        FL = (len(commandList[1]) + 1 )& 0b11111
        #pack the upcode and the file name length
        buffer.append(Opcode+FL)           
        #getting the filename into the buffer
        buffer.extend((commandList[1] +'\n').encode()) 
        if (not os.path.exists(commandList[1])): #if it doesnt exist just create it
            with open(commandList[1],'w') as f:
                    f.write('')
        #getting the file size
        size = os.path.getsize(commandList[1])
        #pack the file size
        buffer.append((size & 0xff000000) >> 24)
        buffer.append((size & 0xff0000) >> 16)
        buffer.append((size & 0xff00) >> 8)
        buffer.append((size & 0xff))
        with open(commandList[1],'r') as f:
            data = f.read()
        buffer.extend(data.encode())        
    #get
    elif (opcode == 'get'):
        Opcode = (1 & 0b111) << 5
        FL = (len(commandList[1]) + 1) & 0b11111 
        buffer.append(Opcode+FL)
        buffer.extend((commandList[1] +'\n').encode())    
    #change
    elif (commandList[0] == "change"):
        Opcode = (2 & 0b111) << 5
        OFL = (len(commandList[1]) + 1) & 0b11111
        NFL = (len(commandList[2]) + 1) & 0xff
        buffer.append(Opcode+OFL)
        buffer.extend((commandList[1]+'\n').encode())
        buffer.append(NFL)
        buffer.extend((commandList[2]+'\n').encode())
    elif (commandList[0] == "bye"):
        print("Session is terminated.")        
        exit()                
    else:
        Opcode = (4 & 0b111) << 5
        buffer.append(Opcode)
    s.send(buffer)

#PART 2 : HANDLE RESPONSE    
    response = s.recv(1024)
    firstByte = response[0]
    rescode = firstByte >> 5
        
    #get   
    if (rescode == 1):        
        FL = firstByte - (Opcode << 5)  & 0b11111         
        FN = response[1:FL+1].decode()[:-1]
        filesize = response[FL] << 24
        filesize += response[FL+1] << 16
        filesize += response[FL+2] << 8
        filesize += response[FL+3]
        # read file data and write it    
        data = response[FL+4:].decode()
        with open(FN,'w') as f:
            f.write(data)       
        if (debugMode):
            print(FN,"has been downloaded successfully.")   
    #help         
    elif (rescode == 6):
        helpData = response[1:].decode()[:-1]
        print(helpData)
        
#PART 3 : DEBUG STUFF            
    if(debugMode): 
        if (rescode == 0):
            print('Response 000 : correct put or change request')
            if(len(commandList)==2):
                print(commandList[1],"has been upploaded successfully.")
            else:
                print(commandList[1],"has been changed into",commandList[2],'.')            
        elif (rescode == 1):
            print('Response 001 : correct get request')        
        elif (rescode == 2):
                print('Response 010 : File Not Found')
        elif (rescode == 3):
                print('Response 011 : Uknown request')
        elif (rescode == 5):            
                print('Response 101 : unsuccessful change')        
        elif (rescode == 6):
            print('Response 110 : <help>')

s.close()
