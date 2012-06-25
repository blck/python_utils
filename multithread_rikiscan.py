#!/usr/bin/env python


#==============================#
#   R1ki Scan by W00rmB00t     #
#	SYN Stealth Scan       #
#     w00rm.b00t@gmail.com     #
#==============================#


import sys
import fcntl
import logging
import getopt
import Queue
import threading
import time

opened = []
closed = []

#---------- worker thread class ----------#
class WorkerThread(threading.Thread):

	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue =  queue

	def run(self):
		src_ip, dst_ip, ini_port, end_port = self.queue.get()
		ip = IP(src = src_ip, dst = dst_ip)

        	#flags: TCP flags, R=RST, S=SYN
        	for port in range(ini_port,end_port+1):

                	TCP_SYN = TCP(sport=RandShort(), dport=port, flags = 'S', seq=0)
                	TCP_SYNACK = sr1(ip/TCP_SYN, timeout=1)
                	if not TCP_SYNACK or TCP_SYNACK.getlayer(TCP).flags != 0x12:
                        	#print "Scanning port "+str(port)+"...: \033[91mclosed\033[0m"
				closed.append(port)

                	else:
                        	##print "Scanning port "+str(port)+"...: \033[92mopen\033[0m"
				opened.append(port)


		self.queue.task_done()

#------------- usage -----------#
def usage():
	
	"""
	Help function
	"""
	
	print "Usage: multithread_rikiscan.py -d dst_ip [-i iface] [-n num_threads] [-f iniport] [-e endport] "
	print "Example: multithread_rikiscan.py -d 127.0.0.1 -i eth0 -n 50"

	sys.exit(1)

#---------- test_iface ----------#
def test_iface(ifname='eth0'):

	""" 
	This method checks if the given interface exists and returns the ip.
	"""

	try:
		sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(sck.fileno(),0x8915,struct.pack('256s', ifname))[20:24])

	except IOError, err:

		print str(err) + ' ('+ifname+')'
		usage()

#------------- main -------------#
def main():

	if os.getuid() != 0:
		print "\033[91mError: You must be root to execute this program!\033[0m"
		sys.exit(1)

	try:
		optlist, args = getopt.getopt(sys.argv[1:], "d:ho:i:n:e:f:", ["help", "output=", "dest=", "iport=", "eport="]) 

	except getopt.GetoptError, err:
		
		print str(err)
		usage()
	
	ini_port = 0
	end_port = 100
	num_threads = 10
	dst_ip = None
	iface = 'eth0'
	output = "rikiscan.out"
	for o, a in optlist:
		if o == "-i":
			iface = a

		elif o == "-n":
			num_threads = int(a) 
		
		elif o in ("-o", "--output"):
			output = a

		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
	
		elif o in ("-d", "--dest"):
			dst_ip = a

		elif o in ("-f", "--iport"):
			ini_port = int(a)

		elif o in ("-e", "--eport"):
			end_port = int(a)
		
		else:
			assert False, "unhandled option"
			usage()

	if dst_ip == None:
		print "\033[91mError: You must specify a destination ip\033[0m"
		usage()
	if ini_port > end_port:
		print "Initial port is bigger than end one... Swapping values"
		tmp_port = ini_port
		ini_port = end_port
		end_port = tmp_port


	src_ip = test_iface(iface)		
	print "Using interface \033[91m%s\033[0m with ip \033[91m%s\033[0m " % (iface, src_ip)

	print "Beginning scan..."

	queue = Queue.Queue()
	offset=(end_port-ini_port)/num_threads #Num of ports per thread
	for me in range(num_threads):
		worker = WorkerThread(queue)
		worker.setDaemon(True)
		worker.start()
		local_ini_port=me*offset
		local_end_port=(me+1)*offset-1
		queue.put((src_ip, dst_ip, local_ini_port, local_end_port))


	queue.join()
	print "\033[91mClosed\033[0m ports: ", closed
	print "\033[92mOpened\033[0m ports: ", opened

#===========================================================#

if __name__== "__main__":
	try:
	        # Disable annoying IPv6 message
        	logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
        	from scapy.all import *
        	conf.verb=0
	except ImportError:
        	print "Could not import scapy, please install python-scapy package."

	main()
