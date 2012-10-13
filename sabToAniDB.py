#!/usr/bin/python

# Author: Benjamin Waller <benjamin@mycontact.eu>
# based on pyanidb

import sys, os
import shlex, subprocess
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser

if len(sys.argv) < 2:
	print "No folder supplied - is this being called from SABnzbd?"
	sys.exit()
else:
	config = {}
	try:
		cp = ConfigParser.ConfigParser()
		cp.read(os.path.join(os.path.dirname(sys.argv[0]), "anidb.cfg"))
		for option in cp.options('integration'):
			config[option] = cp.get('integration', option)
	except:
		pass
	
	command = sys.executable + " " + os.path.join(os.path.dirname(sys.argv[0]), "anidb.py") + " " + config['sabtoanidb_switches'] + " '" + sys.argv[1] + "'"
	if (os.name != "posix"):
		args = shlex.split(command, posix=False)
	else:
		args = shlex.split(command)
	
	retcode = subprocess.call(args)
	
	# For SickBeard integration
	if (os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), config['sabtosickbeard_script'])) == True):
		subprocess.call(sys.argv)
	
	sys.exit(retcode)
