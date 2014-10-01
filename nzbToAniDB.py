#!/usr/bin/python

# Author: Benjamin Waller <benjamin@mycontact.eu>
# based on pyanidb

##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Anime renaming & sync with AniDB.net
#
# This script will rename Anime files after syncing with AniDB.
# Renaming can be done using AniDB or TheTVDB as source.
#
#
# NOTE: Edit "anidb.cfg" in your scripts folder to configure nzbToAniDB
#
#
# NOTE: This script requires Python to be installed on your system.

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import sys, os
import shlex, subprocess
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94
POSTPROCESS_NONE=95

if len(sys.argv) < 2 and not 'NZBPP_DIRECTORY' in os.environ:
	print "No folder supplied"
	sys.exit(1)
else:
	config = {}
	try:
		cp = ConfigParser.ConfigParser()
		cp.read(os.path.join(os.path.dirname(sys.argv[0]), "anidb.cfg"))
		for option in cp.options('integration'):
			config[option] = cp.get('integration', option)
	except:
		pass
	
	if 'NZBPP_DIRECTORY' in os.environ: #NZBGet
		TargetPath=os.environ['NZBPP_DIRECTORY']
	else: # SAB or manual
		TargetPath=sys.argv[1]
		
	if not os.path.exists(TargetPath):
		print('Destination directory does not exist')
		sys.exit(1)
	
	command = sys.executable + " " + os.path.join(os.path.dirname(sys.argv[0]), "nzbToAniDB.libs", "anidb.py") + " " + config['nzbtoanidb_switches'] + " '" + TargetPath + "'"
	if (os.name != "posix"):
		args = shlex.split(command, posix=False)
	else:
		args = shlex.split(command)
	
	retcode = subprocess.call(args)
	
	
	if 'NZBPP_DIRECTORY' in os.environ: #NZBGet
		if retcode == 0:
			retcode = POSTPROCESS_SUCCESS
		else:
			retcode = POSTPROCESS_ERROR

	sys.exit(retcode)
