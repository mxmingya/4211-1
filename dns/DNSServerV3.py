# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os
from socket import *
import os.path

PORT = 5001
HOST = ''


def main():
    try:
        # create a socket object, SOCK_STREAM for TCP
        sSocket = socket(AF_INET, SOCK_STREAM)
    except error as msg:
        # Handle excepton
        sSocket = None
    if sSocket is None:
        print("Error: cannot open socket")
        sys.exit(1)  # If the socket cannot be opened, quit the program.

    try:
        # bind socket to the current address on port 5001, and start to listen to the port
        sSocket.bind((HOST, PORT))
        sSocket.listen(20)
    except error as msg:
        # Handle exception
        print("Error: cannot bind socket to the port")
        sys.exit(1)

    # If the socket cannot be opened, quit the program.
    if sSocket is None:
        print("cannot open socket, quit")
        sys.exit(1)
    # start the control thread, which may terminate the program while encountering input "exit"
    monitor = threading.Thread(target=monitorQuit, args=[])
    monitor.start()
    print("Server is listening...")
    # receive data from user
    while 1:
        # blocked until a remote machine connects to the local port 5001
        connectionSock, addr = sSocket.accept()
        server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
        server.start()
        monitorQuit()


def dnsQuery(connectionSock, srcAddress):
    domainName = connectionSock.recv(1024).decode()
    try:
        line = findIP(domainName, ho)
        if line:
            output = "Local DNS:" + line
        else:
            ip = gethostbyname(domainName)
            file = open("DNS Mapping.txt", "a")
            file.write(domainName + ':' + ip + '\n')
            file.close()
            output = 'Root DNS:{}:{}'.format(domainName, ip)

    except gaierror as msg:
		output = "Host Not Found to the client"
    connectionSock.send(output.encode())
    connectionSock.close()

def findIP(domainName):
    with open("DNS Mapping.txt", "r") as f:
        for line in f:
            check = match(domainName + ':', line)
            if check:
                return line
    return None


def monitorQuit():
    while 1:
        sentence = input()
        if sentence == "exit":
            # os.getpid() returns the parent thread id, which is the id of the main program
            # an hence terminate the main program
            os.kill(os.getpid(), 9)


main()
