#! /usr/bin/env python3
import sys, os
sys.path.append("../../lib")
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "FTServer"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:" , bindAddr)

sock, addr = lsock.accept()

print("connection received from", addr)

while True:

    dataIn = sock.recv(100)
    print(dataIn.decode())
    fileSize, fileName = re.split(":",dataIn.decode())
    if fileName == "exit":
        print("Client disconnected")
        sys.exit(0)
    if os.path.isfile(fileName):
        sock.send(("FILE ALREADY EXISTS").encode())
        dataIn = None
    elif int(fileSize) > 0:
        f = open(fileName, 'wb')
        sock.send(("READY TO RECEIVE").encode())
        dataIn = sock.recv(100)
        totalBytesRecvd = len(dataIn)
        f.write(dataIn)
        
        while totalBytesRecvd < int(fileSize):
            dataIn = sock.recv(100)
            totalBytesRecvd += len(dataIn)
            f.write(dataIn)
            
        print("file transfer complete")
        sock.send(("file transfer complete").encode())

    else:
        print("File is Empty")
        sock.send(("EMPTY FILE").encode())

