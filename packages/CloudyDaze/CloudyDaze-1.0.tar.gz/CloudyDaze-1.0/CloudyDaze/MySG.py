#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, json, logging, requests, urllib, boto.ec2

from collections import namedtuple

from Baubles.Logger import Logger
from Argumental.Argue import Argue

from CloudyDaze.MyAWS import config

for logger in ['boto','urllib3.connectionpool']:
		logging.getLogger(logger).setLevel(logging.ERROR)

logger = Logger()
args = Argue()

#_____________________________________________________
@args.command(single=True)
class MySG(object):

	@args.property(short='p', default='default')
	def profile(self): return

	@args.property(short='u', default='https://api.ipify.org?format=json')
	def url(self): return
	
	@args.property(short='v', flag=True, help='verbose logging')
	def verbose(self): return False

	ports = {
		22: 'tcp',
		443: 'tcp',
		3389: 'tcp',
		1521: 'tcp',
		8888: 'tcp',
	}
	
	types=[
		'tcp',
		'udp',
		'icmp',
		-1
	]

	#_______________________________________________________________
	def __init__(self):
		self.config = config()

		if self.verbose:
			logger.setLevel(logging.DEBUG)
		else:
			logger.setLevel(logging.INFO)

		self.conn = boto.ec2.connect_to_region(
			self.config[self.profile]['region'],
			aws_access_key_id=self.config[self.profile]['aws_access_key_id'],
			aws_secret_access_key=self.config[self.profile]['aws_secret_access_key'],
		)
		
		self.security_group = self.config[self.profile]['mysg']

		self._myip = None

	#_________________________________________________
	def __del__(self):
		self.conn.close()

	
	#_________________________________________________
	def dictate(self, d):
		return '%s:%s'%(
			d['cidr_ip'].split('/')[0],
   			d['to_port']
		)	


	#_________________________________________________
	@args.operation
	def myip(self):
		if not self._myip:
			results = requests.get(self.url).json()
			self._myip = results['ip']
			logger.info('myip = %s'%self._myip)
		return self._myip


	#_________________________________________________
	def __security_group(self):
		for sg in self.conn.get_all_security_groups():
			if sg.id != self.security_group: 
				continue
			logger.debug('sg = %s'% sg)
			return sg


	#_________________________________________________
	@args.operation
	def granted(self):
		_granted = list()
		sg = self.__security_group()
		for rule in sg.rules:
			for grant in rule.grants:
				_grant = dict(
					ip_protocol=str(rule.ip_protocol),
					cidr_ip=str(grant),
					from_port=int(rule.from_port),
					to_port=int(rule.to_port),
				)
				logger.info('authorised = %s'%self.dictate(_grant))
				_granted.append(_grant)
				ip = str(grant).replace('/32','')
		return _granted
	

	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	def enable(self, ips=[]):
		if len(ips) == 0:
			ips = [self.myip()]
		sg = self.__security_group()

		_granted = self.granted()
		_enabled = []
		_todo = list()

		# create list of grants to do
		for ip in ips:
			for port, tipe in self.ports.items():
				if tipe not in self.types:
					sys.stderr.write('%s not in %s\n'%(tipe,self.types))
					continue
				_do = dict(
					ip_protocol=tipe,
					from_port=port,
					to_port=port,
					cidr_ip='%s/32'%ip,
				)
				logger.debug('todo = %s'%self.dictate(_do))
				_todo.append(_do)
		
		# filter out already completed grants
		for _grant in _granted:
			for t in range(len(_todo))[::-1]:
				_do = _todo[t]
				test = map(lambda x: _do[x] == _grant[x], _grant.keys())
				if all(test):
					logger.debug('authorised = %s'%self.dictate(_do))
					_enabled.append(_do)
					del _todo[t]

		# process the remaing todo items
		for _do in _todo:
			logger.info('authorising = %s'%self.dictate(_do))
			_enabled.append(_do)
			sg.authorize(src_group=None,**_do)
			
		return _enabled


	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	@args.parameter(name='forall', short='a', flag=True, help='revoke all')
	def revoke(self, ips=[], forall=False):
		if len(ips) == 0:
			ips = [self.myip()]
		sg = self.__security_group()
		_granted = self.granted()
		_revoked = []
		for ip in ips:
			for _grant in _granted:
				if forall or ip == _grant['cidr_ip'].split('/')[0]:
					_revoked.append(_grant)
					logger.info('revoking = %s'%self.dictate(_grant))
					sg.revoke(
						ip_protocol=_grant['ip_protocol'],
						from_port=_grant['from_port'],
						to_port=_grant['to_port'],
						cidr_ip=_grant['cidr_ip'],
						src_group=None
					)
		
		return _revoked
	

	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	@args.parameter(name='forall', short='a', flag=True, help='revoke all')
	def replace(self, ips=[], forall=False):
		result = dict()
		result['revoked'] = self.revoke(ips, forall)
		result['enabled'] = self.enable(ips)
		return result
		
	
