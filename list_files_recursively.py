import os
import sys

def listFiles(dir='.', s=''):
	basedir=dir
	token = s + '-'
	try:
		for item in os.listdir(dir):
			if os.path.isfile(os.path.join(basedir, item)):
				print token+" "+item
			elif os.path.isdir(os.path.join(basedir,item)):
				print '\033[94m'+token+" "+item+'\033[0m'
				listFiles(os.path.join(basedir, item), token)
	except OSError:
		return	
if len(sys.argv)==1:
	listFiles();
else:
	listFiles(sys.argv[1])

