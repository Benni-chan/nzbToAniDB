import os.path, time, re, urllib2
import xml.etree.ElementTree as ET

tvdbapikey = "A26D3567B57792BD"

class TvDB:
	def __init__(self, animelistfile):
		self.animelistfile = animelistfile
		self.update_anime_list()
		self.animelist = ET.parse(self.animelistfile)
		
	def update_anime_list(self,force=False):
		url  = "https://raw.githubusercontent.com/ScudLee/anime-lists/master/anime-list.xml"
		
		if (force or not os.path.exists(self.animelistfile) or os.path.getmtime(self.animelistfile) < time.time()-(7*24*60*60)):
			print "anime-list.xml too old! Downloading new version..."
			
			u = urllib2.urlopen(url)
			f = open(self.animelistfile, 'wb')
			meta = u.info()
			file_size = int(meta.getheaders("Content-Length")[0])
			print "Downloading: %s Bytes: %s" % (self.animelistfile, file_size)
		
			file_size_dl = 0
			block_sz = 8192
			while True:
				buffer = u.read(block_sz)
				if not buffer:
					break
			
				file_size_dl += len(buffer)
				f.write(buffer)
				status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
				status = status + chr(8)*(len(status)+1)
				print status,
		
			f.close()
	
	# get tvdbid and season/episodenumber for an anidb episode
	def find_tvdb(self,anidbid,anidbepnum):
	
		tvdbseason = None
		tvdbepnum = None
		specialEp = False
		
		while anidbepnum[0] == "0":
			anidbepnum = anidbepnum[1:]
		
		#check if anidbepnum is an multi-ep
		if '-' in anidbepnum:
			firstep = anidbepnum.split('-')[0]
			lastep = anidbepnum.split('-')[1]
			
			if firstep[0] == 'S':
				firstep = firstep[1:]
				specialEp = True
			if lastep[0] == 'S':
				lastep = lastep[1:]
				specialEp = True
			
			eps = []
			for ep in range(int(firstep), int(lastep)+1):
				eps.append(ep)
		else:
			if anidbepnum[0] == 'S':
				anidbepnum = anidbepnum[1:]
				specialEp = True
			try:
				eps = {int(anidbepnum)}
			except:
				return None
		
		item = self.animelist.find("./anime[@anidbid='"+anidbid+"']")
		
		if item == None:
			return None
		
		tvdbid = item.attrib['tvdbid']
		tvdbepnums = []
		for ep in eps:
			tvdbepnum = str(ep) #default, can be overwritten by mapping below
			tvdbseason = item.attrib['defaulttvdbseason'] #default, can be overwritten by mapping below
			
			if ( specialEp ):
				anidbseason = '0'
				tvdbseason = '0' #default, can be overwritten by mapping below
			else:
				anidbseason = '1'
			
			mappinglist = item.findall("./mapping-list/mapping[@anidbseason='"+anidbseason+"']")
			if mappinglist != None:
				for map in mappinglist:
					result = re.match("(.*);"+str(ep)+"-([0-9]*)(.*)", map.text)
					if result != None:
						tvdbepnum = result.group(2)
						tvdbseason = map.attrib['tvdbseason']
						break
		
			#handle absolute episode mapping
			if tvdbseason == 'a' and anidbseason == '1':
				absoluteurl = "http://thetvdb.com/api/"+tvdbapikey+"/series/"+tvdbid+"/absolute/"+str(ep)+"/en.xml"
				episodedata = ET.fromstring(urllib2.urlopen(absoluteurl).read())
				tvdbseason = episodedata.find("./Episode/SeasonNumber").text
				tvdbepnum = episodedata.find("./Episode/EpisodeNumber").text
			
			if None in (tvdbid,tvdbseason,tvdbepnum):
				return None
		
			seriesurl = "http://thetvdb.com/api/"+tvdbapikey+"/series/"+tvdbid+"/en.xml"
			episodeurl = "http://thetvdb.com/api/"+tvdbapikey+"/series/"+tvdbid+"/default/"+tvdbseason+"/"+tvdbepnum+"/en.xml"
		
			try:
				seriesdata
			except NameError:
				try:
					seriesdata = ET.fromstring(urllib2.urlopen(seriesurl).read())
				except urllib2.HTTPError, e:
					return None


			try:
				episodedata
			except NameError:
				try:
					episodedata = ET.fromstring(urllib2.urlopen(episodeurl).read())
				except urllib2.HTTPError, e:
					return None

			tvdbseason = "%02d" % (int(tvdbseason))	
			tvdbepnum = "%02d" % (int(tvdbepnum))
			tvdbepnums.append(tvdbepnum)
		
		return {'tvdbid':tvdbid, 'tvdbseason': tvdbseason, 'tvdbepnum': tvdbepnums, 'tvdbseriesname': seriesdata.find("./Series/SeriesName").text, 'tvdbepname': episodedata.find("./Episode/EpisodeName").text}
		