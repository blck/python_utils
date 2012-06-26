#!/usr/bin/env python


import signal
import getopt
import socket
import sys

def ctrlc_handler(signum, frm):

	print "Ha! You cannot kill me!! =)"



def alarm_handler(signum, frm):

	print "Riiiiing!!!"
	sys.exit(0)


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
		s = socket.socket()
		s.bind(('',65000))
		s.listen(0)

		(client,(ip, port))=s.accept()
		client.send("Welcome to simple echo server!\n")

		signal.alarm(sec)	

		while True:
			data = client.recv(2048)
			print "client sent:", data
			client.send(data)	

	else:
		sys.exit(0)

