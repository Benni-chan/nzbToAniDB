import threading, time, os, hashlib, binascii
try:
	import xattr
except ImportError:
	xattr = None

class Ed2k:
	def __init__(self):
		self.md4_partial = hashlib.new('md4')
		self.md4_final = hashlib.new('md4')
		self.size_total = 0
	
	def update(self, data):
		pos = 0
		while pos < len(data):
			if (not (self.size_total % 9728000)) and self.size_total:
				self.md4_final.update(self.md4_partial.digest())
				self.md4_partial = hashlib.new('md4')
			size = min(len(data) - pos, 9728000 - (self.size_total % 9728000))
			self.md4_partial.update(data[pos:pos + size])
			pos += size
			self.size_total += size
	
	def hexdigest(self):
		if self.size_total > 9728000:
			self.md4_final.update(self.md4_partial.digest())
			return self.md4_final.hexdigest()
		return self.md4_partial.hexdigest()

class Crc32:
	def __init__(self):
		self.s = 0
	
	def update(self, data):
		self.s = binascii.crc32(data, self.s)
	
	def hexdigest(self):
		return '{0:08x}'.format(self.s & 0xffffffff)

hasher_obj = {
	'ed2k': Ed2k,
	'md5': lambda: hashlib.new('md5'),
	'sha1': lambda: hashlib.new('sha1'),
	'crc32': Crc32,
}

class Hash:
	def __init__(self, filename, algorithms):
		update_list = []
		for a in algorithms:
			h = hasher_obj[a]()
			update_list.append(h.update)
			setattr(self, a, h.hexdigest)
		
		f = open(filename, 'rb')
		data = f.read(131072)
		while data:
			for u in update_list:
				u(data)
			data = f.read(131072)

class File:
	def __init__(self, name, algorithms, cache):
		self.name = name
		self.size = os.path.getsize(name)
		self.mtime = os.path.getmtime(name)
		self.cached = False
		if cache:
			print "test"
			self.read_cache()
		if False in [hasattr(self, a) for a in algorithms]:
			self.cached = False
			h = Hash(name, algorithms)
			for a in algorithms:
				setattr(self, a, getattr(h, a)())
			if cache: self.write_cache()
	
	def read_cache(self):
		if not xattr:
			return
		cache = dict([(n[13:], xattr.get(self.name, n)) for n in xattr.list(self.name) if n.decode().startswith('user.anidb.')])
		if 'mtime' not in cache or str(int(self.mtime)) != cache.pop('mtime'):
			return
		for n, v in cache.items():
			setattr(self, n, v)
		self.cached = True
	
	def write_cache(self):
		if not xattr:
			return
		try:
			self.clear_cache()
			xattr.set(self.name, 'user.anidb.mtime', str(int(self.mtime)))
			for n in ('ed2k', 'md5', 'sha1', 'crc32'):
				if hasattr(self, n):
					xattr.set(self.name, 'user.anidb.' + n, getattr(self, n))
		except IOError:
			pass
	
	def clear_cache(self):
		for name in xattr.list(self.name):
			if name.decode().startswith('user.anidb.'):
				xattr.remove(self.name, name)

class Hashthread(threading.Thread):
	def __init__(self, filelist, hashlist, algorithms, cache, *args, **kwargs):
		self.filelist = filelist
		self.hashlist = hashlist
		self.algorithms = algorithms
		self.cache = cache
		threading.Thread.__init__(self, *args, **kwargs)
	def run(self):
		try:
			while 1:
				f = self.filelist.pop(0)
				self.hashlist.append(File(f, self.algorithms, self.cache))
		except IndexError:
			return

def hash_files(files, cache = False, algorithms = ('ed2k',), num_threads = 1):
	hashlist = []
	threads = []
	for x in range(num_threads):
		thread = Hashthread(files, hashlist, algorithms, cache)
		thread.start()
		threads.append(thread)
	while hashlist or sum([thread.isAlive() for thread in threads]):
		try:
			yield hashlist.pop(0)
		except IndexError:
			time.sleep(0.1)
	raise StopIteration
