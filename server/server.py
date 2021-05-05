import socket
import sys
import os

#PART 0 : CONNECT
HOST = socket.gethostname()  # Standard loopback interface address (localhost)
PORT = 8500 # Port to listen on (non-privileged ports are > 1023)
address = socket.gethostbyname(HOST)        
debugMode =  True if sys.argv[1] == '1' else False 

s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((address, PORT))
s.listen()

print('Server listening on address ',address, 'port number : ', PORT)

#PART 1 : HANDLE COMMAND
while True:
    buffer = bytearray()
    conn, addr = s.accept()        
    print('Connected by', addr)        
    command = conn.recv(1024)
    firstByte = command[0] 
    opcode = firstByte >> 5
        
    #put    
    if (opcode == 0):        
        FL = firstByte - (opcode << 5)     
        FN = command[1:FL+1].decode()[:-1]        
        size = command[FL+1] << 24
        size += command[FL+2] << 16
        size += command[FL+3] << 8
        size += command[FL+4]
        data = command[FL+5:size+FL+6].decode()          
        with open(FN,'w') as f:
            f.write(data)
        if (debugMode):
            print(FN," has been uploaded successfully")
        rescode = (0& 0b111) << 5
        buffer.append(rescode)      
    #get
    elif (opcode == 1):
        FL = firstByte - (opcode << 5) & 0b11111  
        FN = command[1:FL+1].decode()[:-1]
        if (os.path.exists(FN)):
            rescode = (1 & 0b111) << 5 
            buffer.append(rescode+FL)
            buffer.extend(FN.encode())
            size = os.path.getsize(FN)
            buffer.append((size & 0xff000000) >> 24)
            buffer.append((size & 0xff0000) >> 16)
            buffer.append((size & 0xff00) >> 8)
            buffer.append((size & 0xff))
            with open(FN,'r') as f:
                data = f.read()                            
            buffer.extend(data.encode())
        else:
            rescode = (2& 0b111) << 5
            buffer.append(rescode)   
    #change
    elif (opcode == 2): 
        OFL = firstByte - (opcode << 5) & 0b11111  
        OFN = command[1:OFL+1].decode()[:-1]
        NFL = command[OFL+1]
        NFN = command[OFL+2:OFL+3+NFL].decode()[:-1]
        if (os.path.exists(OFN)):
            try:
                os.rename(OFN,NFN)
                rescode = (0& 0b111) << 5
                buffer.append(rescode)
                if (debugMode):
                    print(OFN , " changed to ", NFN)
            except:
                rescode = (5& 0b111) << 5
                buffer.append(rescode) 
                if(debugMode):
                    print(OFN, ' rename to ', NFN, "couldn't be completed")
        else: 
            rescode = (2& 0b111) << 5
            buffer.append(rescode) 
    #help
    elif (opcode == 3):
        rescode = (6 & 0b111) << 5
        response = "Commands are: bye change get help put\n" 
        length = (len(response) & 0b11111) 
        buffer.append(rescode+length) 
        buffer.extend(response.encode())
    else:
        rescode = (3& 0b111) << 5
        buffer.append(rescode)               

    conn.send(buffer)  
      
    #PART 2 : SHOW DEBUG RESPONSE    
    if(debugMode):   
        print('Transaction made successfully')     
        if (rescode == 0):            
            print('Response 000 sent : correct put or change request')
        elif(rescode == 1):
            print('Response 001 sent : correct get request')
            print(FN,"has been upploaded successfully.")       
        elif(rescode==2):
            print('Response 010 sent : ',FN,' File Not Found')    
        elif (rescode==3):
            print('Response 011 sent : unknown request')
        elif (rescode==5):
            print('Response 101 sent : unsuccessful change')
        elif(rescode==6):
            print('Response 011 sent : <help command>')               
        print("The message is sent successfully")
conn.close()