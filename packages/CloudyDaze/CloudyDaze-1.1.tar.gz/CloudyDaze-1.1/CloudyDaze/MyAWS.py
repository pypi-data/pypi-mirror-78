#!/usr/bin/env python3

import os, logging

from configparser import ConfigParser

def silence():
	for logger in [
		'boto',
		'botocore.auth',
		'botocore.hooks',
   		'botocore.client',
		'botocore.endpoint',
   		'botocore.parsers',
   		'botocore.loaders',
   		'botocore.credentials',
		'botocore.retryhandler',
		'boto3.resources.action',
		'boto3.resources.factory',
   		'paramiko.transport',
		'urllib3.connectionpool'
	]:
		logging.getLogger(logger).setLevel(logging.ERROR)

		
#___________________________________________________________________
def config(home='~/'):
	'''
	return a dict of the .aws files { profile: { key: value }	}
	'''
	
	parser = ConfigParser()

	for file in ['credentials','config']:
		dot_aws = os.path.expanduser('%s/.aws/%s'%(home,file))
		if os.path.exists(dot_aws):
			parser.read(dot_aws)	
				
	result = dict.fromkeys(parser.sections())
	for key in result.keys():
		result[key] = dict()
		for (name,value) in parser.items(key):
			result[key][name] = value

	return result

