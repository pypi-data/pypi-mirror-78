#!/usr/bin/env python3

import os

from configparser import ConfigParser

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

