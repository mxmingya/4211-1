# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os
from socket import *
import os.path

PORT = 5001
def main():

	try:
		#create a socket object, SOCK_STREAM for TCP
		s = socket(AF_INET, SOCK_STREAM)
	except error as msg:
		# Handle exception
		s = None
	if s is None:
		print("Error: cannot open socket")
		sys.exit(1) # If the socket cannot be opened, quit the program.

	try:
		#bind socket to the current address on port 5001,
		#TODO:look for host name in directory first
		host = s.gethostbyname()#if local hostname is not found in the directory
		s.bind((host, PORT))
		s.listen(20)#Listen on the given socket maximum number of connections queued is 20
	except error as msg:
		# Handle exception
		print("Error: cannot bind socket to the port")
		sys.exit(1)

	# If the socket cannot be opened, quit the program.
	if s is None:
		print("cannot open socket, quit")
		sys.exit(1)
	#start the control thread, which may terminate the program while encountering input "exit"
	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()
	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port 5001
		connectionSock, addr = s.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

def dnsQuery(connectionSock, srcAddress):
	#read line by line from the client host
	#Begin to check the query
	#If the query is "hangup" close the socket
	#Extract domain name.
	with connectionSock:
		print('Connected by', srcAddress)
		while True:
			query = connectionSock.recv(1024)
			#create the local directory if doesnt exist
			if not os.path.isfile("DNS Mapping.txt"):
				file = open("DNS Mapping.txt", "a")
			if not query:
				break
			if query == "":
				continue
			elif:
				query == "hangup"
				print("signal received, closing the socket")
				connectionSock.close()
			elif:
				#parse the query and shoot
				domainName = query
	try:
		#First, check local DNS which is a file you created when the first query was successfully resolved(e.g. DNS_mapping.txt)
		#If you find the result in this file, return the result with the appropriate format to the client
	    	#If the host name was not found in the local DNS file ,use the local machine DNS lookup and if found return it to the client
			#also add the result to the local DNS file
		for line in file:#TODO:check if the file is here
			
	except:
		#If the host name was not found, return "Host Not Found to the client"
	#Close the server socket

def monitorQuit():
	while 1:
		sentence = input()
		if sentence == "exit":
			#os.getpid() returns the parent thread id, which is the id of the main program
			#an hence terminate the main program
			os.kill(os.getpid(),9)

main()
