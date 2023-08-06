#!/usr/bin/env python3

import sys, re, os, uuid, json, logging, urllib
from time import sleep

import boto
import boto.ec2
import boto.ec2.elb

from Baubles.Logger import Logger
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config

for logger in ['boto','urllib3.connectionpool']:
		logging.getLogger(logger).setLevel(logging.ERROR)

logger = Logger()
args = Argue()
	
#_________________________________________________
@args.command(single=True)
class MyEC2(object):

	@args.property(short='p', default='default')
	def profile(self): return

	@args.property(short='v', flag=True, help='verbose logging')
	def verbose(self): return False

	def __init__(self):
		self.config = config()
		self.conn = boto.ec2.connect_to_region(
			self.config[self.profile]['region'],
			aws_access_key_id=self.config[self.profile]['aws_access_key_id'],
			aws_secret_access_key=self.config[self.profile]['aws_secret_access_key'],
		)

		
	def __del__(self):
		self.close()
		

	def close(self):
		self.conn.close()

		
	@args.operation
	@args.parameter(name='ids', short='i', nargs='*', help='aws ec2 id list')
	def list(self, ids=[]):
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				if len(ids) > 0 and instance.id not in ids: continue
				if self.verbose:
					printp(json.dumps(dir(instance),indent=4))
					print(instance.ip_address)
				if str(instance.state) not in status.keys():
					status[str(instance.state)] = list()
				status[str(instance.state)].append(str(instance.id))
		return status

		
	@args.operation
	@args.parameter(name='ids', short='i', nargs='*', help='aws ec2 id list')
	def start(self, ids=[]):
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				logger.info(instance)
				if len(ids) > 0 and instance.id not in ids: continue
				if instance.state not in [ u'pending', u'starting', u'running' ]:
					instance.start()
					logger.info(instance)
				if str(instance.state) not in status.keys():
					status[str(instance.state)] = list()
				status[str(instance.state)].append(str(instance.id))
		return status

		
	@args.operation
	@args.parameter(name='ids', short='i', nargs='*', help='aws ec2 id list')
	def stop(self, ids=[]):
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				logger.info(instance)
				if len(ids) > 0 and instance.id not in ids: continue
				if instance.state not in [ u'pending', u'stopping', u'stopped' ]:
					instance.stop()
					logger.info(instance)
				if str(instance.state) not in status.keys():
					status[str(instance.state)] = list()
				status[str(instance.state)].append(str(instance.id))
		return status
		
