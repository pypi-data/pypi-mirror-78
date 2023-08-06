#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import re, os, sys, socket, paramiko

from Baubles.Logger import Logger
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config, silence

silence()

logger = Logger()
squirrel = Squirrel()
args = Argue()

	
#___________________________________________________________________
@args.command(single=True)
class MySSH(object):

	@args.property(short='u')
	def username(self): return

	@args.property(short='H')
	def hostname(self): return
	
	@args.property(short='p')
	def password(self): return
	
	@args.property(short='P', type=int, default=22)
	def port(self): return 22
		
	@args.property(short='k', help='ssh key path')
	def key(self): return None
	
	@args.property(short='t', type=int, default=5, help='connect timeout seconds')
	def timeout(self): return None
	
	@args.property(short='v', flag=True, help='verbose logging')
	def verbose(self): return False

	def __init__(self):
		self.client = paramiko.SSHClient()		
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy()
		)
		self.connected = False

	def connect(self):
		if self.connected:
			return

		# force ip4 host connect
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.hostname, self.port))
		
		if self.key:
			privateKey = paramiko.RSAKey.from_private_key_file(
				os.path.expanduser(self.key), 
				password=self.password
			)
			self.client.connect(
				self.hostname,
				sock=sock,
				port=self.port, 
				username=self.username,
				pkey=privateKey,
				timeout=self.timeout,
			)
		else:
			self.client.connect(
				self.hostname, 
				sock=sock,
				port=self.port, 
				username=self.username, 
				password=self.password, 
				timeout=self.timeout,
			)

		self.connected = True

	def __del__(self):
		self.close()
		

	def close(self):
		self.connected = False
		if self.client:
			self.client.close()
		

	@args.operation
	@args.parameter(name='phrase', short='c', help='execute command string')
	def execute(self, phrase=''):
		self.connect()
		print('$ %s' % phrase)
		stdin, stdout, stderr = self.client.exec_command(phrase)
		sys.stderr.write(str(stderr.read()))
		return str(stdout.read())
		

#___________________________________________________________________
def test():
	mySSH = MySSH()
	mySSH.username = 'ubuntu'
	mySSH.hostname = 'pocketrocketsoftware.com'
	mySSH.password = squirrel.get('ssh:%s:%s'%(
		mySSH.username,
		mySSH.hostname
	)) 
	mySSH.key = '~/.ssh/id_rsa'

	mySSH.connect()
	print(mySSH.execute('whoami'))
	print(mySSH.execute('uptime'))
	mySSH.close()

