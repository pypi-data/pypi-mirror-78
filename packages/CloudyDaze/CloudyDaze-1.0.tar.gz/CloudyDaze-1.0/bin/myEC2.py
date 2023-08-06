#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, json

sys.path.append('..')

from Baubles.Logger import Logger
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config
from CloudyDaze.MyEC2 import MyEC2, args

print(json.dumps(args.execute(), indent=4))

