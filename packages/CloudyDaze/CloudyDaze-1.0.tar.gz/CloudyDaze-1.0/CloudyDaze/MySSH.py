#!/usr/bin/env python

import re, os, sys, socket, paramiko

from Tools.Squirrel import Squirrel

squirrel = Squirrel()


class MySSH(object):
	def __init__(self, username, hostname, password=None, port=22, key=None):
		
		# force ip4 host connect
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((hostname, port))
		
		self.client = paramiko.SSHClient()		
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy()
		)
		
		if key:
			privateKey = paramiko.RSAKey.from_private_key_file(
				os.path.expanduser(key), password=password
			)
			self.client.connect(
				hostname,
				sock=sock,
				port=port, 
				username=username,
				pkey=privateKey,
				timeout=5,
			)
		else:
			self.client.connect(
				hostname, 
				sock=sock,
				port=port, 
				username=username, 
				password=password, 
				timeout=5,
			)

	def __del__(self):
		self.close()

	def close(self):
		self.client.close()

	def execute(self, command):
		print('$ %s' % command)
		stdin, stdout, stderr = self.client.exec_command(command)
		sys.stderr.write(stderr.read())
		return stdout.read()


def main():
	username = 'ubuntu'
	hostname = 'pocketrocketsoftware.com'
	password = squirrel.get('ssh:%s:%s'%(
		username,
		hostname,
	)) 
	key = '~/.ssh/id_rsa'
	mySSH = MySSH(
		username, 
		hostname, 
		key=key, 
		password=password,
	)
	print(mySSH.execute('uptime'))
	#print(mySSH.execute('cd ~/tmp; ls -s;'))
	mySSH.close()


if __name__ == '__main__': main()
	
