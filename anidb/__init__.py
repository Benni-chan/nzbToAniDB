import socket, time

protover = 3
client = 'sabnzbdplugin'
clientver = 1

states = {
	'unknown': 0,
	'hdd': 1,
	'cd': 2,
	'deleted': 3,
	'shared': 4,
	'release': 5}

fcode = (
	'', 'aid', 'eid', 'gid', 'lid','depr', 'state',
	'size', 'ed2k', 'md5', 'sha1', 'crc32',
	'quality', 'source', 'acodec', 'abitrate', 'vcodec', 'vbitrate', 'vres', 'filetype',
	'dublang', 'sublang', 'length', 'description', 'airdate', 'anifilename')

acode = (
	'eptotal', 'eplast', 'year', 'type', 'category',
	'romaji', 'kanji', 'english', 'other', 'short', 'synonym',
	'epno', 'epname', 'epromaji', 'epkanji', 'gname', 'gtag')
	

info = fcode + acode
#info = dict([(info[i], 1 << i) for i in range(len(info)) if info[i]])

class AniDBError(Exception):
	pass

class AniDBTimeout(AniDBError):
	pass

class AniDBLoginError(AniDBError):
	pass

class AniDBUserError(AniDBLoginError):
	pass

class AniDBReplyError(AniDBError):
	pass

class AniDBUnknownFile(AniDBError):
	pass

class AniDBNotInMylist(AniDBError):
	pass

class AniDBUnknownAnime(AniDBError):
	pass

class AniDBUnknownDescription(AniDBError):
	pass

class AniDB:
	def __init__(self, username, password, localport = 1234, server = ('api.anidb.info', 9000)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('0.0.0.0', localport))
		self.sock.settimeout(10)
		self.username = username
		self.password = password
		self.server = server
		self.session = ''
		self.lasttime = 0
	
	def __del__(self):
		self.logout()
		self.sock.close()
	
	def newver_msg(self):
		print('New version available.')
	
	def retry_msg(self):
		print('Connection timed out, retrying.')
	
	def execute(self, cmd, args = None, retry = False):
		if not args:
			args = {}
		while 1:
			data = '{0} {1}\n'.format(cmd, '&'.join(['{0}={1}'.format(*a) for a in args.items()]))
			t = time.time()
			if t < self.lasttime + 2:
				time.sleep(self.lasttime + 2 - t)
			self.lasttime = time.time()
			self.sock.sendto(data.encode(), 0, self.server)
			try:
				data = self.sock.recv(8192).decode().split('\n')
			except socket.timeout:
				if retry:
					self.retry_msg()
				else:
					raise AniDBTimeout()
			else:
				break
		code, text = data[0].split(' ', 1)
		data = [line.split('|') for line in data[1:-1]]
		code = int(code)
		return code, text, data
	
	def ping(self):
		t = time.time()
		try:
			return self.execute('PING')[0] == 300 and time.time() - t or None
		except AniDBTimeout:
			return None
	
	def auth(self):
		code, text, data = self.execute('AUTH', {'user': self.username, 'pass': self.password, 'protover': protover, 'client': client, 'clientver': clientver})
		if code in (200, 201):
			self.session = text.split(' ', 1)[0]
			if code == 201:
				self.newver_msg()
		elif code == 500:
			raise AniDBUserError()
		else:
			raise AniDBReplyError(code, text)
	
	def logout(self):
		if self.session:
			try:
				self.execute('LOGOUT', {'s': self.session})
				self.session = ''
			except AniDBError:
				pass
	
	def get_file(self, fid, retry = False):
		try:
			size, ed2k = fid
			args = {'size': size, 'ed2k': ed2k}
		except TypeError:
			args = {'fid': fid}
		info_codes = list(info)
		args.update({'s': self.session, 'fmask': '7FF8FFF9', 'amask': 'F2FCF0C0'})
		while 1:
			code, text, data = self.execute('FILE', args, retry)
			if code == 220:
				return dict([(name, data[0].pop(0)) for name in ['fid'] + info_codes])
			elif code == 320:
				raise AniDBUnknownFile()
			elif code in (501, 506):
				self.auth()
			else:
				raise AniDBReplyError(code, text)
	
	def add_file(self, fid, state = None, viewed = False, source = None, storage = None, other = None, edit = False, retry = False):
		try:
			size, ed2k = fid
			args = {'size': size, 'ed2k': ed2k}
		except TypeError:
			args = {'fid': fid}
		if not edit and state == None:
			state = 'hdd'
		if state != None:
			args['state'] = states[state]
		if viewed != None:
			args['viewed'] = int(bool(viewed))
		if source != None:
			args['source'] = source
		if storage != None:
			args['storage'] = storage
		if other != None:
			args['other'] = other
		if edit:
			args['edit'] = 1
		args['s'] = self.session
		while 1:
			code, text, data = self.execute('MYLISTADD', args, retry)
			if code in (210, 310, 311):
				return
			elif code == 320:
				raise AniDBUnknownFile()
			elif code == 411:
				raise AniDBNotInMylist()
			elif code in (501, 506):
				self.auth()
			else:
				raise AniDBReplyError(code, text)

	def get_anime(self, aid = None, aname = None, amask = None, retry = False):
		args = {}
		if not aid == None:
			args['aid'] = aid
		elif not aname == None:
			args['aname'] == aname
		else:
			raise TypeError('must set either aid or aname')

		args['amask'] = amask or '00'*7
		args['s'] = self.session

		while 1:
			code, text, data = self.execute('ANIME', args, retry)
			if code == 230:
				return data[0]
			elif code == 330:
				raise AniDBUnknownAnime()
			elif code in (501, 506):
				self.auth()
			else:
				raise AniDBReplyError(code, text)

	def get_animedesc(self, aid, retry = False):
		args = {'aid': aid, 'part': 0, 's': self.session}
		description = ''
		while 1:
			code, text, data = self.execute('ANIMEDESC', args, retry)
			if code == 233:
				curpart, maxpart, desc = data[0]
				description += desc
				if curpart == maxpart:
					return description
				else:
					args['part'] = int(curpart)+1
			elif code == 330:
				raise AniDBUnknownAnime()
			elif code == 333:
				raise AnidBUnknownDescription()
			elif code in (501, 506):
				self.auth()
			else:
				raise AniDBReplyError(code, text)
