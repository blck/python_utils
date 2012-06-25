#!/usr/bin/env python

import os
import getopt
import sys

def usage():

	print "Usage: list_files_recursively.py [-d dir] [-r]"
	print "Example: list_files_recursively.py -d /home -r"
	sys.exit(1)

def listFiles(dir='.', s='', r=False):
	basedir=dir
	token = s + '-'
	it = ''
	try:
		for item in os.listdir(dir):
			it = item
			if os.path.isfile(os.path.join(basedir, item)):
				print token+" "+item
			elif os.path.isdir(os.path.join(basedir,item)):
				print '\033[94m'+token+" "+item+'\033[0m'
				if r:
					listFiles(os.path.join(basedir, item), token, True)
	except OSError, err:
		print str(err)+", skipping..."
		return


def main():

	try:
                optlist, args = getopt.getopt(sys.argv[1:], "d:r", ["help"])

        except getopt.GetoptError, err:

                print str(err)
                usage()


	d='.'
	recursive = False
	for o, a in optlist:
		if o == "-d":
			d=a
		elif o == "-r":
			recursive = True
		elif o == "--help":
			usage()
		else:
			assert False, "unhandled option"
			usage()

	listFiles(d, r = recursive)





if __name__ == "__main__":
	main()
