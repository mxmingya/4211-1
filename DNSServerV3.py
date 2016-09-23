# Fall 2016 CSci4211: Introduction to Computer Networks
# This program serves as the server of DNS query.
# Written in Python v3.

import sys, threading, os
from socket import *

def main():

	try:
		#create a socket object, SOCK_STREAM for TCP	
	except error as msg:
		# Handle exception

	try:
		#bind socket to the current address on port 5001
		#Listen on the given socket maximum number of connections queued is 20
	except error as msg:
		# Handle exception

	# If the socket cannot be opened, quit the program.
	
	#start the control thread, which may terminate the program while encountering input "exit"
	monitor = threading.Thread(target=monitorQuit, args=[])
	monitor.start()

	print("Server is listening...")

	while 1:
		#blocked until a remote machine connects to the local port 5001
		connectionSock, addr = sSock.accept()
		server = threading.Thread(target=dnsQuery, args=[connectionSock, addr[0]])
		server.start()

def dnsQuery(connectionSock, srcAddress):
	#read line by line from the client host
	#Begin to check the query	
	#If the query is "hangup" close the socket
	#Extract domain name.

	try:
		#First, check local DNS which is a file you created when the first query was successfully resolved(e.g. DNS_mapping.txt) 
		#If you find the result in this file, return the result with the appropriate format to the client  	
	    	#If the host name was not found in the local DNS file ,use the local machine DNS lookup and if found return it to the client
			#also add the result to the local DNS file
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
