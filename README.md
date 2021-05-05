# README
## About
This is a program that simulates a **typical FTP interaction between a client and a server**. The server and the client are each in a separate folder for demonstration purposes.

Both client and server programs support a final command-line argument as a **debug flag** that turns on/off printing of the messages sent and received. `0` means Debug mode is OFF and  `1` means Debug
mode is ON.
## prerequisites
to use this piece of software you should make sure to install the latest version of python3, it wasn't tested on other versions.
## Steps
1. To test the program you must run both the server and the client:
    - The server, to be able to listen to incoming requests
    - The client to be able to send requests
*Please note that you must run the server only once per multiple client sessions*

2. To run the server, navigate to the server directory and type the following command
3. `python3 server.py 1` -->   *(the 1 flag here indicates that debug mode is ON, you can choose an option)*.
    - When the program runs, it will output a string similar to the following: `Server listening on address  169.254.29.240 port number:  8500` 
4.  navigate to the client directory and type the following command
`python3 client [HOST] [PORT].py 0` -->   *(the 0 flag here indicates that debug mode is OFF, you can choose an option)*.
    - copy paste the host address and port number from the server's output
5. The client accepts input lines that consist of one request. User commands are:
    - put *filename* (to upload from client to server)
    - get *filename* (to download from client to server)
    - change *oldfilename* *newfilename* (to change the names on the server)
    - help (to print the available commands)
    - bye (to close the session and exit the client program)
7. The `tests` directory contains two sample scripts, run these scripts and check your server and client folders for the results
