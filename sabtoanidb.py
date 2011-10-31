#!/usr/bin/python

# Author: Benjamin Waller <benjamin@mycontact.eu>
# based on pyanidb

import sys, os


if len(sys.argv) < 2:
	print "No folder supplied - is this being called from SABnzbd?"
	sys.exit()
else:
	command= os.path.join(os.path.dirname(sys.argv[0]), "anidb.py")
	os.system(command +" -r -n -m -a -w -x '" + sys.argv[1]+"'")
	