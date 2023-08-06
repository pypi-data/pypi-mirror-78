#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, json

sys.path.append('..')

from Baubles.Logger import Logger
from Argumental.Argue import Argue

from CloudyDaze.MyAWS import config
from CloudyDaze.MySG import MySG, args

args.execute()
