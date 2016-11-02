import sys, socket, threading, select, hashlib
import threading, os


def server(host, port):
    PORT = int(port)
    copied = open('download.txt', 'w')
    expectSeq = 0
    try:
        sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object, SOCK_STREAM for TCP
    except error as msg:
        sSock = None # Handle exception

    try:
        sSock.bind(('', PORT)) #bind socket to the current address on port 5001
        sSock.listen(20) #Listen on the given socket maximum number of connections queued is 20
    except error as msg:
        sSock = None # Handle exception
    if sSock is None:
        print("Error: cannot open socket")
        sys.exit(1) # If the socket cannot be opened, quit the program.
    # monitor = threading.Thread(target=monitorQuit, args=[])
    # monitor.start()
    print("Server is listening...")
    connection, addr = sSock.accept()
    print('connected')
    while 1:
        packet = connection.recv(512).decode()
        hash_object = hashlib.sha1(packet[40:].encode())
        checkSumInPac = hash_object.hexdigest()
        checkSum = packet[0:40]
        if checkSum != checkSumInPac:
            print('checksum error')
            continue
        checkSum, seq, actualSize, isLast, actualData, allData = parsePacket(packet)

        ACK = makePacket('', seq, isLast)
        connection.send(ACK.encode())
        if seq == expectSeq:
            if isLast == 1:
                copied.close()
                print('here')
                os.rename('download.txt', actualData)
                os.kill(os.getpid(),9)
            else:
                copied.write(actualData)
                expectSeq = (expectSeq + 1) % 100
                print('expectSeq is: ', expectSeq)
        else:
            if seq != expectSeq:
                print('seq error')
            continue



def client(host, port, filename):
	nameOfFile = filename.split('/')[-1]
	timeOut = 1
	file = open(filename, 'r')

	seqNumToSend = 0
	ackExpected = 0
	state = 1

	try:
		cSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except error as msg:
		cSock = None # Handle exception
	try:
		cSock.connect((host, int(port)))
	except error as msg:
		cSock = None # Handle exception
	if cSock is None:
		print("Error: cannot open socket")
		sys.exit(1) # If the socket cannot be opened, quit the program.
	store = file.read(466)
	while True:
		if state == 1:
			fin = 0

			if store:
				packet = makePacket(store, seqNumToSend, fin)
				sp = parsePacket(packet)
				ackExpected = seqNumToSend
				state = 0
				cSock.send(packet.encode()) # Otherwise, send the input to server.
			else:
				fin = 1
				packet = makePacket(nameOfFile, seqNumToSend, fin)
				ackExpected = seqNumToSend
				state = 0
				cSock.send(packet.encode()) # Otherwise, send the input to server.
		elif state == 0:
			ready = select.select([cSock], [], [], timeOut)
			if ready[0]:
				data = cSock.recv(512).decode()
				#receive ack, check the checkSum
				timeOut = timeOut * 0.9


				hash_object = hashlib.sha1(data[40:].encode())
				checkSumInPac = hash_object.hexdigest()
				checkSum = data[0:40]
				if checkSum != checkSumInPac:
					state = 0
					continue

				if ackPacket[1] == ackExpected:
					# the ack is expected, so change the seqNumToSend
					# also change the state
					seqNumToSend = (seqNumToSend + 1) % 100
					store = file.read(466)
					state = 1
					if ackPacket[3] == 1:
						print('file is done')
					else:
						pass
				else:
					# reveive a wrong packet, send the packet again
					# so change the state and continus directly
					state = 0
					continue
			else:
				state = 0
				timeOut = timeOut * 1.5
				print("Timeout! Retransmitting...")
				continue
		else:
			print('think about why you get this meassage')
	file.close()



def makePacket(data, expectSeq, fin):
	#make packet or ACK based on what we received.
    seqNo = str(expectSeq)
	seqNo = seqNo.zfill(2)

	size = str(hex(len(data)))
	size = size[2:]
	actualSize = size.zfill(3) #fill size with '0' if len(size) is less then 3

	checkIfLast = str(fin)
	allData = seqNo + actualSize + checkIfLast + data.ljust(466, '0')#fill data with '0' if len(data) is less then 466

	checkSum = makeCheckSum(allData.encode())
	return checkSum + allData


def parsePacket(packet):
    checkSum = packet[0:40]
    seq = int(packet[40:42])
    actualSize = int(packet[42:45], 16)
    isLast = int(packet[45:46])
    actualData = packet[46:46 + actualSize]
    allData = packet[40:]
    return checkSum, seq, actualSize, isLast, actualData, allData

def monitorQuit():
    while 1:
        sentence = input()
        if sentence == "exit":
            #os.getpid() returns the parent thread id, which is the id of the main program
            #an hence terminate the main program
            os.kill(os.getpid(),9)

def makeCheckSum(data):
	hash_object = hashlib.sha1(allData.encode())
	return hash_object.hexdigest()


def main():
	if len(sys.argv) == 4:
		[pad, host, port, filename] = sys.argv
		client(host, port, filename)
	elif len(sys.argv) == 3:
		[pad, host, port] = sys.argv
		server(host, port)

main()
