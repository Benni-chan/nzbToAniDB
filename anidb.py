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
except:
	pass

# Options.

op = optparse.OptionParser()

op.add_option('-u', '--username', help = 'AniDB username.',
	action = 'store', dest = 'username', default = config.get('username'))
op.add_option('-p', '--password', help = 'AniDB password.',
	action = 'store', dest = 'password', default = config.get('password'))

op.add_option('-r', '--recursive', help = 'Recurse into directories.',
	action = 'store_true', dest = 'recursive', default = False)
op.add_option('-s', '--suffix', help = 'File suffix for recursive matching.',
	action = 'append', dest = 'suffix', default = config.get('suffix', '').split())
op.add_option('-c', '--no-cache', help = 'Do not use cached values.',
	action = 'store_false', dest = 'cache', default = int(config.get('cache', '0')))

op.add_option('-l', '--multihash', help = 'Calculate additional checksums.',
	action = 'store_true', dest = 'multihash', default = False)
op.add_option('-i', '--identify', help = 'Identify files.',
	action = 'store_true', dest = 'identify', default = False)
op.add_option('-a', '--add', help = 'Add files to mylist.',
	action = 'store_true', dest = 'add', default = False)
op.add_option('-w', '--watched', help = 'Mark files watched.',
	action = 'store_true', dest = 'watched', default = False)

op.add_option('-n', '--rename', help = 'Rename files.',
	action = 'store_true', dest = 'rename', default = False)
op.add_option('-m', '--move', help = 'Move Files',
	action = 'store_true', dest = 'move', default = False)
op.add_option('-x', '--delete', help = 'Delete Folders after moving files',
	action = 'store_true', dest = 'delete', default = False)

op.add_option('-d', '--directory', help = 'Target parent directory.',
	action = 'store', dest = 'directory', default = config.get('directory'))

op.add_option('-o', '--no-color', help = 'Disable color output.',
	action = 'store_false', dest = 'color', default = True)


options, args = op.parse_args(sys.argv[1:])


# Colors.

if options.color:
	red    = lambda x: '\x1b[1;31m' + x + '\x1b[0m'
	green  = lambda x: '\x1b[1;32m' + x + '\x1b[0m'
	yellow = lambda x: '\x1b[1;33m' + x + '\x1b[0m'
	blue   = lambda x: '\x1b[1;34m' + x + '\x1b[0m'
else:
	red    = lambda x: x
	green  = lambda x: x
	yellow = lambda x: x
	blue   = lambda x: x


# Defaults.

if options.cache:
	try:
		import xattr
	except ImportError:
		print(red('No xattr, caching disabled.'))
		options.cache = False
options.identify = options.identify or options.rename or options.move
options.login = options.add or options.watched or options.identify
if not options.suffix:
	options.suffix = ['avi', 'ogm', 'mkv', 'mp4']

if options.login:
	if not options.username:
		options.username = input('Username: ')
	if not options.password:
		options.password = getpass.getpass()

if not options.directory and options.move:
	print(red('No target directory.'))
	sys.exit(1)
	
if not options.move and options.delete:
	print(red('Can\'t delete folder without moving files.'))
	sys.exit(1)

# Input files.

files = []
remaining = deque(args)
while remaining:
	name = remaining.popleft()
	name = name.replace("'", "")
	if not os.access(name, os.R_OK):
		print('{0} {1}'.format(red('Invalid file:'), name))
	elif os.path.isfile(name):
		files.append(name)
	elif os.path.isdir(name):
		if not options.recursive:
			print('{0} {1}'.format(red('Is a directory:'), name))
		else:
			for sub in sorted(os.listdir(name)):
				if os.name == "posix" and sub.startswith('.'):
					continue
				sub = os.path.join(name, sub)
				if os.path.isfile(sub) and any(sub.lower().endswith('.' + suffix) for suffix in options.suffix):
					files.append(sub)
				elif os.path.isdir(sub):
					remaining.appendleft(sub)

if not files:
	print(blue('Nothing to do.'))
	sys.exit(0)

# Authorization.

if options.login:
	a = anidb.AniDB(options.username, options.password)
	try:
		a.auth()
		print('{0} {1}'.format(blue('Logged in as user:'), options.username))
	except anidb.AniDBUserError:
		print(red('Invalid username/password.'))
		sys.exit(1)
	except anidb.AniDBTimeout:
		print(red('Connection timed out.'))
		sys.exit(1)
	except anidb.AniDBError as e:
		print('{0} {1}'.format(red('Fatal error:'), e))
		sys.exit(1)

# Hashing.

hashed = unknown = 0

for file in anidb.hash.hash_files(files, options.cache, (('ed2k', 'md5', 'sha1', 'crc32') if options.multihash else ('ed2k',))):
	print('{0} ed2k://|file|{1}|{2}|{3}|{4}'.format(blue('Hashed:'),  file.name, file.size, file.ed2k, ' (cached)' if file.cached else ''))
	fid = (file.size, file.ed2k)
	hashed += 1
	
	try:
		
		# Multihash.
		if options.multihash:
			print('{0} {1}'.format(blue('MD5:'), file.md5))
			print('{0} {1}'.format(blue('SHA1:'), file.sha1))
			print('{0} {1}'.format(blue('CRC32:'), file.crc32))
		
		# Identify.
		
		if options.identify:
			info = a.get_file(fid, True)
			fid = int(info['fid'])
			
			if (info['english'] == ""): info['english'] = info['romaji']
			
			print('{0} [{1}] {2} ({3}) - {4} - {5} ({6})'.format(green('Identified:'), info['gtag'], info['romaji'], info['english'], info['epno'], info['epromaji'], info['epname']))
						
		# Renaming.
		
		if options.rename or options.move:
			if options.rename:
				
				rename = {}
				try:
					cp = ConfigParser.ConfigParser()
					cp.read(os.path.join(os.path.dirname(sys.argv[0]), "anidb.cfg"))
					for option in cp.options('rename'):
						rename[option] = cp.get('rename', option)
				except:
					pass
								
				#s = options.format
				if (info['type'] == 'Movie' and rename['movieformat']):
					s = rename['movieformat']
				elif (info['type'] == 'OVA' and rename['ovaformat']):
					s = rename['ovaformat']
				elif (rename['tvformat']):
					s = rename['tvformat']
				else:
					s = '%ATe% - %EpNo%%Ver% - %ETe% [%GTs%][%FCRC%]'
				
				rename_data = {
					#Anime title, r: romaji, e: english, k: kanji, s: synonym, o: other
					'ATr': info['romaji'],
					'ATe': info['english'],
					'ATk': info['kanji'],
					'ATs': info['synonym'],
					'ATo': info['other'],
				
					#Episode title, languages as above
					'ETr': info['epromaji'],
					'ETe': info['epname'],
					'ETk': info['epkanji'],
				
					#Group title, s: short, l: long
					'GTs':info['gtag'],
					'GTl':info['gname'],
				
					'EpHiNo': info['eptotal'], #Highest (subbed) episode number
					'EpCount': info['eptotal'], #Anime Episode count
					'AYearBegin': info['year'].split("-")[0],
					'AYearEnd':  info['year'].split("-")[1] if (info['year'].find('-') > 0) else '', #The beginning & ending year of the anime
					'ACatList': info['category'],
				
					'EpNo': info['epno'], #File's Episode number
				
					'Type': info['type'], #Anime type, Value: 'Movie', 'TV', 'OVA', 'Web'
					'Depr': info['depr'], #File is deprecated if the value is '1'
					'Cen': {0:'',1:'1'}[(int(info['state']) & 128)], #File is censored if the value is '1'
					'Ver': {0: '', 4: 'v2', 8: 'v3', 16: 'v4', 32: 'v5'}[(int(info['state']) & 0x3c)], #File version
					'Source': info['source'], #Where the file came from (HDTV, DTV, WWW, etc)
					'Quality': info['quality'], #How good the quality of the file is (Very Good, Good, Eye Cancer)
					'AniDBFN': info['anifilename'], #Default AniDB filename
					'CurrentFN': os.path.basename(file.name), #Current Filename
					'FCrc' : info['crc32'],#The file's crc
					'FCRC': info['crc32'].upper(),
					'FVideoRes': info['vres'], #Video Resolution (e.g. 1920x1080)
					'FALng': info['dublang'], #List of available audio languages (japanese, english'japanese'german)
					'FSLng': info['sublang'], #List of available subtitle languages (japanese, english'japanese'german)
					'FACodec': info['acodec'], #Codecs used for the Audiostreams
					'FVCodec': info['vcodec'], #Codecs used for the Videostreams
					'suf': info['filetype']}
				
				# parse s to replace tags
				for name, value in rename.items():
					s = s.replace(r'%' + name + r'%', value)
				
				for name, value in rename_data.items():
					s = s.replace(r'%' + name + r'%', value)
				
				s = s + '.' + rename_data['suf']
				
				# change spaces to underscores, if first character in s is an underscore
				if s[0] == '_':
					s = s[1:].replace(' ', '_')
			
			if options.move:
				move = {}
				try:
					cp = ConfigParser.ConfigParser()
					cp.read(os.path.join(os.path.dirname(sys.argv[0]), "anidb.cfg"))
					for option in cp.options('move'):
						move[option] = cp.get('move', option)
				except:
					pass
								
				#s = options.format
				if (move['foldername']):
					f = move['foldername']
				else:
					f = '%ATe%'
				
				move_data = {
					#Anime title, r: romaji, e: english, k: kanji, s: synonym, o: other
					'ATr': info['romaji'],
					'ATe': info['english'],
					'ATk': info['kanji'],
					'ATs': info['synonym'],
					'ATo': info['other'],
				
					#Group title, s: short, l: long
					'GTs':info['gtag'],
					'GTl':info['gname'],
				
					'EpHiNo': info['eptotal'], #Highest (subbed) episode number
					'EpCount': info['eptotal'], #Anime Episode count
					'AYearBegin': info['year'].split("-")[0],
					'AYearEnd':  info['year'].split("-")[1] if (info['year'].find('-') > 0) else '', #The beginning & ending year of the anime
					'ACatList': info['category'],
					
					'Type': info['type'], #Anime type, Value: 'Movie', 'TV', 'OVA', 'Web'
					'Source': info['source'], #Where the file came from (HDTV, DTV, WWW, etc)
					'Quality': info['quality'], #How good the quality of the file is (Very Good, Good, Eye Cancer)
					'FVideoRes': info['vres'], #Video Resolution (e.g. 1920x1080)
					'FALng': info['dublang'], #List of available audio languages (japanese, english'japanese'german)
					'FSLng': info['sublang'], #List of available subtitle languages (japanese, english'japanese'german)
					'FACodec': info['acodec'], #Codecs used for the Audiostreams
					'FVCodec': info['vcodec'], #Codecs used for the Videostreams
					'suf': info['filetype']}
				
				# parse f to replace tags
				for name, value in move.items():
					f = f.replace(r'%' + name + r'%', value)
				
				for name, value in move_data.items():
					f = f.replace(r'%' + name + r'%', value)
				
				# change spaces to underscores, if first character in s is an underscore
				if f[0] == '_':
					f = f[1:].replace(' ', '_')
			
			
			#do the rename and move
				
			filename = os.path.basename(file.name)
			
			if (options.rename):
				if (os.name == "posix"):
					filename = s.replace('/', '_').replace(':', ' -')
				else:
					filename = s.replace('/', '_').replace('\\', '_').replace(':', ' -').replace('*', '_').replace('?', '_').replace('"', '\'').replace('<', '_').replace('>', '_').replace('|', '_')
				while filename.startswith('.'):
					filename = filename[1:]
				print('{0} {1}'.format(yellow('Renaming to:'), filename))
				path = os.path.dirname(file.name)
				
			if (options.move):
				if (os.name == "posix"):
					subdir = f.replace('/', '_').replace(':', ' -')
				else:
					subdir = f.replace('/', '_').replace('\\', '_').replace(':', ' -').replace('*', '_').replace('?', '_').replace('"', '\'').replace('<', '_').replace('>', '_').replace('|', '_')
				while subdir.startswith('.'):
					subdir = subdir[1:]
				path = os.path.join(options.directory, subdir)
				print('{0} {1}'.format(yellow('Moving to:'), path))
				if (os.path.exists(path) == False):
					os.umask(0007)
					os.mkdir(path,0770)
			
			shutil.move(file.name, os.path.join(path,filename))
		
		if options.delete:
			delete_folder = True
			folder = os.path.dirname(file.name)
			for sub in sorted(os.listdir(folder)):
				sub = os.path.join(folder, sub)
				if os.path.isfile(sub) and any(sub.lower().endswith('.' + suffix) for suffix in options.suffix) or os.path.isdir(sub):
					#don't delete
					delete_folder = False
			
			if delete_folder:
				shutil.rmtree(folder)
		
		
		# Adding.
		
		if options.add:
			a.add_file(fid, viewed = options.watched, retry = True)
			print(green('Added to mylist.'))
		
		# Watched.
		
		elif options.watched:
			a.add_file(fid, viewed = True, edit = True, retry = True)
			print(green('Marked watched.'))
		
	except anidb.AniDBUnknownFile:
		print(red('Unknown file.'))
		unknown += 1
	
	except anidb.AniDBNotInMylist:
		print(red('File not in mylist.'))

# Finished.

print(blue('Hashed {0} files{1}.'.format(hashed, ', {0} unknown'.format(unknown) if unknown else '')))
if (unknown > 0):
	sys.exit(1)
