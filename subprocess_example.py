#!/usr/bin/python

import subprocess

subprocess.call(['ls', '-l'])

subprocess.check_output(['ls', '-l'])


handle = subprocess.Popen(["ls", '-l'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

print handle.stdout.read()
