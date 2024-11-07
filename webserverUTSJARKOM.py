#import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Ready to serve...")

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # Receive message from the client
        message = connectionSocket.recv(1024).decode()
        
        # Extract the filename from the HTTP request
        filename = message.split()[1]
        f = open(filename[1:], "r")  # Remove the leading '/' from filename
        outputdata = f.read()

        # Send HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())
        
        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data