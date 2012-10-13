#!/usr/bin/env python

# Author: Benjamin Waller <benjamin@mycontact.eu>
# based on pyanidb

import anidb, anidb.hash
try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser
import optparse, os, sys, getpass, shutil
from collections import deque

is_array = lambda var: isinstance(var, (list, tuple))

# Workaround for input/raw_input
if hasattr(__builtins__, 'raw_input'):
	input = raw_input

# Config.

config = {}
try:
	cp = ConfigParser.ConfigParser()
	cp.read(os.path.join(os.path.dirname(sys.argv[0]), "anidb.cfg"))
	for option in cp.options('AniDB'):
		config[option] = cp.get('AniDB', option)
	
	for option in cp.options('rename'):
		rename[option] = cp.get('rename', option)
except:
	pass


color = True

# Colors.

if color:
	red    = lambda x: '\x1b[1;31m' + x + '\x1b[0m'
	green  = lambda x: '\x1b[1;32m' + x + '\x1b[0m'
	yellow = lambda x: '\x1b[1;33m' + x + '\x1b[0m'
	blue   = lambda x: '\x1b[1;34m' + x + '\x1b[0m'
else:
	red    = lambda x: x
	green  = lambda x: x
	yellow = lambda x: x
	blue   = lambda x: x


def authorize_with_anidb(auth_username, auth_password):
	a = anidb.AniDB(auth_username, auth_password)
	try:
		a.auth()
		print('{0} {1}'.format(blue('Logged in as user:'), auth_username))
	except anidb.AniDBUserError:
		print(red('Invalid username/password.'))
		sys.exit(1)
	except anidb.AniDBTimeout:
		print(red('Connection timed out.'))
		sys.exit(1)
	except anidb.AniDBError as e:
		print('{0} {1}'.format(red('Fatal error:'), e))
		sys.exit(1)


def hash_files(files, multiHash=False, cache=False):
	if not is_array(files):
		myfiles = []
		myfiles.append(files)
	else:
		myfiles = files
	
	hashes = anidb.hash.hash_files(myfiles, cache, (('ed2k', 'md5', 'sha1', 'crc32') if multiHash else ('ed2k',)))
	
	for file in hashes:
		print('{0} ed2k://|file|{1}|{2}|{3}|{4}'.format(blue('Hashed:'),  file.name, file.size, file.ed2k, ' (cached)' if file.cached else ''))
		fid = (file.size, file.ed2k)
		
		if multiHash:
			print('{0} {1}'.format(blue('MD5:'), file.md5))
			print('{0} {1}'.format(blue('SHA1:'), file.sha1))
			print('{0} {1}'.format(blue('CRC32:'), file.crc32))
	

def identify(fid):
	try:
		info = a.get_file(fid, True)
		fid = int(info['fid'])
			
		if (info['english'] == ""): info['english'] = info['romaji']
			
		print('{0} [{1}] {2} ({3}) - {4} - {5} ({6})'.format(green('Identified:'), info['gtag'], info['romaji'], info['english'], info['epno'], info['epromaji'], info['epname']))
	
	except anidb.AniDBUnknownFile:
		print(red('Unknown file.'))
		#unknown += 1
	


def process_file(filepath):
	hash_files("/Volumes/Media/Anime/Nodame Cantabile/Nodame Cantabile - 01 - Lesson 1 [A-Keep][1280x720][DTV][F1D3D2F7].mkv")
	
	
	return 0


def process_path(path):
	if not os.access(path, os.R_OK):
		print('{0} {1}'.format(red('Invalid file:'), path))
	else:
		files = []
		for sub in sorted(os.listdir(path)):
			if os.name == "posix" and sub.startswith('.'):
				continue
			sub = os.path.join(name, sub)
			if os.path.isfile(sub) and any(sub.lower().endswith('.' + suffix) for suffix in options.suffix):
				files.append(sub)
			elif os.path.isdir(sub):
				remaining.appendleft(sub)
	
	
	
	files.append("/Volumes/Media/Anime/Nodame Cantabile/Nodame Cantabile - 01 - Lesson 1 [A-Keep][1280x720][DTV][F1D3D2F7].mkv")
	files.append("/Volumes/Media/Anime/Nodame Cantabile/Nodame Cantabile - 02 - Lesson 2 [A-Keep][1280x720][DTV][67D24450].mkv")
	hash_files(files)
	
	return 0





