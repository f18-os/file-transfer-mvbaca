#! /usr/bin/env python3

import sys
sys.path.append("../../lib")       # for params
import re, socket, params, os


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

sock = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        sock = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        sock = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        sock.connect(sa)
    except socket.error as msg:
        print(" e rror: %s" % msg)
        sock.close()
        sock = None
        continue
    break

if sock is None:
    print('could not open socket')
    sys.exit(1)

    
endClient = False
while not endClient:
    fileName = input("What file would you like to send? ->")
    if fileName == "exit":
        sock.send("0:exit".encode())
        sys.exit(0)
    elif os.path.isfile(fileName):
        size = os.path.getsize(fileName)
        sock.send((str(size)+":"+fileName).encode())
        serverMsg = sock.recv(100).decode()
        if serverMsg == "READY TO RECEIVE":
            print("Server: "+serverMsg)
            with open(fileName, 'rb') as f:
                bytesToSend = f.read(100)
                sock.send(bytesToSend)
                while bytesToSend.decode() != "":
                    bytesToSend = f.read(100)
                    sock.send(bytesToSend)
                    print(bytesToSend.decode())

            print("done sending file\n")
            print("Server: "+sock.recv(100).decode())
            
        elif serverMsg == "FILE ALREADY EXISTS":
            print("server already has the file "+fileName)
        elif serverMsg == "EMPTY FILE":
            print("File "+fileName+" is empty")
    else:
        print("File does not exist")
