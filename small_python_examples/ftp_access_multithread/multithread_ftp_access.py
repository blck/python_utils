#!/usr/bin/env python

import sys
import Queue
import threading
import ftplib
from ftplib import FTP
import time
import getopt

class WorkerThread(threading.Thread):
	
	def __init__(self, id, queue):

		threading.Thread.__init__(self)
		self.queue = queue
		self.id = id


	def run(self):

		l = []
		ftpSites = self.queue.get()
		for site in ftpSites:
			l.append("Elements in \033[92m%s\033[0m:" % site.strip())
			ftp = FTP(site.strip())
			ftp.login()
			ftp.retrlines('LIST', l.append)
			ftp.quit()

		lock.acquire()
		print "I'm thread %d and my server list is: " % self.id, ftpSites
		for e in l:
			print e
		print "#########################"	
		lock.release()
		
		self.queue.task_done()

def usage():

	print "Usage: multithread_ftp_access.py [-i input_file] [-n num_threads]"
        print "Example: multithread_ftp_access.py -i ftp_list.txt -n 10"

        sys.exit(1)

	
def main():

	try:
                optlist, args = getopt.getopt(sys.argv[1:], "n:i:", ["help"])

        except getopt.GetoptError, err:

                print str(err)
                usage()

	
	input_file = "ftp_list.txt"
	num_threads = 1

	for o, a in optlist:
        	if o == "-i":
                	input_file = a

                elif o == "-n":
                        num_threads = int(a)

                else:
                        assert False, "unhandled option"
                        usage()

	queue = Queue.Queue()
        servers = open("ftp_list.txt","r").readlines()
	offset=(len(servers)/num_threads)
	for me in range(num_threads):
		worker = WorkerThread(me,queue)
		worker.setDaemon(True)
		worker.start()
		local_ftp_sites = servers[me*offset:(me+1)*offset]
		queue.put(local_ftp_sites)


	queue.join()

if __name__ == "__main__":

	lock = threading.Lock() 
	main()
	
	
		
