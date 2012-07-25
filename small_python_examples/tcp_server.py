#!/usr/bin/env python


import signal
import getopt
import socket
import sys
import threading
import Queue
import time

def ctrlc_handler(signum, frm):

	print "Ha! You cannot kill me!! =)"



def alarm_handler(signum, frm):

	print "Riiiiing!!!"
	sys.exit(0)




class Server_Thread(threading.Thread):

	def __init__(self, client_sock, ip):

		threading.Thread.__init__(self)
		self.client_socket = client_sock

	def run(self):

		data = 'dummy'
                while len(data):        #this is to exit when the client disconnects
                        data = self.client_socket.recv(2048)
                        print "client %s sent:" % ip, data
                        self.client_socket.send(data)



if __name__ == "__main__":

	args, opt = getopt.getopt(sys.argv[1:],"t:")
	sec = 0
	for arg, opt in args:
		sec = int(opt)

	print "Installing signal handlers..."
	signal.signal(signal.SIGINT, ctrlc_handler)
	signal.signal(signal.SIGALRM, alarm_handler)
	print "Done"

	if(sec):
	
		print "Server will end after %d seconds..." % sec
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET => inet family, STREAM => TCP, DGRAM=>UDP
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #sets reuse addr to 1

		s.bind(('0.0.0.0',65000)) #Now we've created the socket, we have to bind the socket to a port and specific interface
		s.listen(2) #Once socket is binded to a port, we start listening =). The parameter is the number of concurrent clients that the socket can handle.

		while True:
			(client,(ip, port))=s.accept() # Start waiting for clients. Blocking call
		#Return values:
		#client => new socket created for the client connected
		#(ip,port) => ip and port of the client	


			server_thread = Server_Thread(client,ip)
			server_thread.setDaemon(True)
			server_thread.start()
			client.send("\033[091mWelcome to simple echo server!\033[0m\n")

		#signal.alarm(sec)	


	else:
		sys.exit(0)
