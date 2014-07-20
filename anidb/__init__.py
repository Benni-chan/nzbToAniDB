import socket, time

protover = 3
client = 'nzbtoanidb'
clientver = 1

states = {
	'unknown': 0,
	'hdd': 1,
	'cd': 2,
	'deleted': 3,
	'shared': 4,
	'release': 5
	}

fcode = (
	'aid', 'eid', 'gid', 'lid', 'depr', 'state',
	'crc32', 'vcdepth',
	'quality', 'source', 'acodec', 'abitrate', 'vcodec', 'vbitrate', 'vres', 'filetype',
	'dublang', 'sublang', 'length', 'airdate', 'anifilename'
	)

acode = (
	'eptotal', 'eplast', 'year', 'type',
	'romaji', 'kanji', 'english',
	'epno', 'epname', 'epromaji', 'epkanji',
	'gname', 'gtag'
	)

info = fcode + acode
#info = dict([(info[i], 1 << i) for i in range(len(info)) if info[i]])

LOGIN_ACCEPTED                           = 200
LOGIN_ACCEPTED_NEW_VERSION               = 201
LOGGED_OUT                               = 203
RESOURCE                                 = 205
STATS                                    = 206
TOP                                      = 207
UPTIME                                   = 208
ENCRYPTION_ENABLED                       = 209
MYLIST_ENTRY_ADDED                       = 210
MYLIST_ENTRY_DELETED                     = 211
ADDED_FILE                               = 214
ADDED_STREAM                             = 215
EXPORT_QUEUED                            = 217
EXPORT_CANCELLED                         = 218
ENCODING_CHANGED                         = 219
FILE                                     = 220
MYLIST                                   = 221
MYLIST_STATS                             = 222
WISHLIST                                 = 223
NOTIFICATION                             = 224
GROUP_STATUS                             = 225
WISHLIST_ENTRY_ADDED                     = 226
WISHLIST_ENTRY_DELETED                   = 227
WISHLIST_ENTRY_UPDATED                   = 228
MULTIPLE_WISHLIST                        = 229
ANIME                                    = 230
ANIME_BEST_MATCH                         = 231
RANDOM_ANIME                             = 232
ANIME_DESCRIPTION                        = 233
REVIEW                                   = 234
CHARACTER                                = 235
SONG                                     = 236
ANIMETAG                                 = 237
CHARACTERTAG                             = 238
EPISODE                                  = 240
UPDATED                                  = 243
TITLE                                    = 244
CREATOR                                  = 245
NOTIFICATION_ENTRY_ADDED                 = 246
NOTIFICATION_ENTRY_DELETED               = 247
NOTIFICATION_ENTRY_UPDATE                = 248
MULTIPLE_NOTIFICATION                    = 249
GROUP                                    = 250
CATEGORY                                 = 251
BUDDY_LIST                               = 253
BUDDY_STATE                              = 254
BUDDY_ADDED                              = 255
BUDDY_DELETED                            = 256
BUDDY_ACCEPTED                           = 257
BUDDY_DENIED                             = 258
VOTED                                    = 260
VOTE_FOUND                               = 261
VOTE_UPDATED                             = 262
VOTE_REVOKED                             = 263
HOT_ANIME                                = 265
RANDOM_RECOMMENDATION                    = 266
RANDOM_SIMILAR                           = 267
NOTIFICATION_ENABLED                     = 270
NOTIFYACK_SUCCESSFUL_MESSAGE             = 281
NOTIFYACK_SUCCESSFUL_NOTIFIATION         = 282
NOTIFICATION_STATE                       = 290
NOTIFYLIST                               = 291
NOTIFYGET_MESSAGE                        = 292
NOTIFYGET_NOTIFY                         = 293
SENDMESSAGE_SUCCESSFUL                   = 294
USER_ID                                  = 295
CALENDAR                                 = 297

PONG                                     = 300
AUTHPONG                                 = 301
NO_SUCH_RESOURCE                         = 305
API_PASSWORD_NOT_DEFINED                 = 309
FILE_ALREADY_IN_MYLIST                   = 310
MYLIST_ENTRY_EDITED                      = 311
MULTIPLE_MYLIST_ENTRIES                  = 312
WATCHED                                  = 313
SIZE_HASH_EXISTS                         = 314
INVALID_DATA                             = 315
STREAMNOID_USED                          = 316
EXPORT_NO_SUCH_TEMPLATE                  = 317
EXPORT_ALREADY_IN_QUEUE                  = 318
EXPORT_NO_EXPORT_QUEUED_OR_IS_PROCESSING = 319
NO_SUCH_FILE                             = 320
NO_SUCH_ENTRY                            = 321
MULTIPLE_FILES_FOUND                     = 322
NO_SUCH_WISHLIST                         = 323
NO_SUCH_NOTIFICATION                     = 324
NO_GROUPS_FOUND                          = 325
NO_SUCH_ANIME                            = 330
NO_SUCH_DESCRIPTION                      = 333
NO_SUCH_REVIEW                           = 334
NO_SUCH_CHARACTER                        = 335
NO_SUCH_SONG                             = 336
NO_SUCH_ANIMETAG                         = 337
NO_SUCH_CHARACTERTAG                     = 338
NO_SUCH_EPISODE                          = 340
NO_SUCH_UPDATES                          = 343
NO_SUCH_TITLES                           = 344
NO_SUCH_CREATOR                          = 345
NO_SUCH_GROUP                            = 350
NO_SUCH_CATEGORY                         = 351
BUDDY_ALREADY_ADDED                      = 355
NO_SUCH_BUDDY                            = 356
BUDDY_ALREADY_ACCEPTED                   = 357
BUDDY_ALREADY_DENIED                     = 358
NO_SUCH_VOTE                             = 360
INVALID_VOTE_TYPE                        = 361
INVALID_VOTE_VALUE                       = 362
PERMVOTE_NOT_ALLOWED                     = 363
ALREADY_PERMVOTED                        = 364
HOT_ANIME_EMPTY                          = 365
RANDOM_RECOMMENDATION_EMPTY              = 366
RANDOM_SIMILAR_EMPTY                     = 367
NOTIFICATION_DISABLED                    = 370
NO_SUCH_ENTRY_MESSAGE                    = 381
NO_SUCH_ENTRY_NOTIFICATION               = 382
NO_SUCH_MESSAGE                          = 392
NO_SUCH_NOTIFY                           = 393
NO_SUCH_USER                             = 394
CALENDAR_EMPTY                           = 397
NO_CHANGES                               = 399

NOT_LOGGED_IN                            = 403
NO_SUCH_MYLIST_FILE                      = 410
NO_SUCH_MYLIST_ENTRY                     = 411
MYLIST_UNAVAILABLE                       = 412

LOGIN_FAILED                             = 500
LOGIN_FIRST                              = 501
ACCESS_DENIED                            = 502
CLIENT_VERSION_OUTDATED                  = 503
CLIENT_BANNED                            = 504
ILLEGAL_INPUT_OR_ACCESS_DENIED           = 505
INVALID_SESSION                          = 506
NO_SUCH_ENCRYPTION_TYPE                  = 509
ENCODING_NOT_SUPPORTED                   = 519
BANNED                                   = 555
UNKNOWN_COMMAND                          = 598

INTERNAL_SERVER_ERROR                    = 600
ANIDB_OUT_OF_SERVICE                     = 601
SERVER_BUSY                              = 602
NO_DATA                                  = 603
TIMEOUT_DELAY_AND_RESUBMIT               = 604
API_VIOLATION                            = 666

PUSHACK_CONFIRMED                        = 701
NO_SUCH_PACKET_PENDING                   = 702


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
		if code in (LOGIN_ACCEPTED, LOGIN_ACCEPTED_NEW_VERSION):
			self.session = text.split(' ', 1)[0]
			if code == LOGIN_ACCEPTED_NEW_VERSION:
				self.newver_msg()
		elif code == LOGIN_FAILED:
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
		args.update({'s': self.session})
		#'fmask': '7BFAFFF900', 'amask': 'F2FCF0C0'
		
		args.update({'fmask': '7B0AFFE900'})
		args.update({'amask': 'F0E0F0C0'})
		
		while 1:
			code, text, data = self.execute('FILE', args, retry)
			if code == FILE:
				return dict([(name, data[0].pop(0)) for name in ['fid'] + info_codes])
			elif code == NO_SUCH_FILE:
				raise AniDBUnknownFile()
			elif code in (LOGIN_FIRST, INVALID_SESSION):
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
			if code in (MYLIST_ENTRY_ADDED, FILE_ALREADY_IN_MYLIST, MYLIST_ENTRY_EDITED):
				return
			elif code == NO_SUCH_FILE:
				raise AniDBUnknownFile()
			elif code == NO_SUCH_MYLIST_ENTRY:
				raise AniDBNotInMylist()
			elif code in (LOGIN_FIRST, INVALID_SESSION):
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
			if code == ANIME:
				return data[0]
			elif code == NO_SUCH_ANIME:
				raise AniDBUnknownAnime()
			elif code in (LOGIN_FIRST, INVALID_SESSION):
				self.auth()
			else:
				raise AniDBReplyError(code, text)

	def get_animedesc(self, aid, retry = False):
		args = {'aid': aid, 'part': 0, 's': self.session}
		description = ''
		while 1:
			code, text, data = self.execute('ANIMEDESC', args, retry)
			if code == ANIME_DESCRIPTION:
				curpart, maxpart, desc = data[0]
				description += desc
				if curpart == maxpart:
					return description
				else:
					args['part'] = int(curpart)+1
			elif code == NO_SUCH_ANIME:
				raise AniDBUnknownAnime()
			elif code == NO_SUCH_DESCRIPTION:
				raise AnidBUnknownDescription()
			elif code in (LOGIN_FIRST, INVALID_SESSION):
				self.auth()
			else:
				raise AniDBReplyError(code, text)
