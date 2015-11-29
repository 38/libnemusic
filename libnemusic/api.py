# -*- coding: utf-8 -*-
import network
from rpc import RemoteResult, RPCMethod, RPCFunction
import model
import encode
import random
import sys

####### Album ############
class AlbumDetailResult(RemoteResult):
	class album(model.NamedObject):
		class artists(model.List): Element = model.RequireModel('Artist')
		size = model.Integer
		company = model.String
		class songs(model.List): Element = model.RequireModel('SongInfo')
	
class Album(model.NamedObject):
	artist = model.RequireModel('Artist')
	company = model.String
	@RPCMethod("GET", "api/album/", AlbumDetailResult)
	def details(self):
		return {"__suffix__" : self.id}

class AlbumSearchResult(RemoteResult):
	class result(model.Dictionary):
		albumCount = model.Integer
		class albums(model.List): Element = model.RequireModel('Album')

###### Artists #########
class ArtistInfo(model.NamedObject):
	pass

class ArtistDetialResult(RemoteResult):
	artist = model.RequireModel('ArtistInfo')
	class hotSongs(model.List): Element = model.RequireModel('SongInfo')
	more   = model.Boolean

class Artist(model.NamedObject): 
	@RPCMethod("GET", "api/artist/", ArtistDetialResult)
	def details(self):
		return {"__suffix__" : self.id}

class ArtistSearchResult(RemoteResult):
	class result(model.Dictionary):
		artistCount = model.Integer
		class artists(model.List): Element = model.RequireModel('Artist')

###### Songs ###############
class Mp3Info(model.NamedObject):
	size      = model.Integer
	extension = model.String
	dfsId     = model.Integer
	playTime  = model.Integer
	biterate  = model.Integer
	def geturl(self):
		return "http://m%s.music.126.net/%s/%s.mp3" % (random.randrange(1, 3), encode.encode_id(str(self.dfsId)) , self.dfsId)

class SongInfo(model.NamedObject):
	mp3Url    = model.String
	class artists(model.List): Element = model.RequireModel('Artist')
	hMusic    = model.RequireModel('Mp3Info')
	mMusic    = model.RequireModel('Mp3Info')
	lMusic    = model.RequireModel('Mp3Info')
	def __getitem__(self, quality):
		if quality == "high" and self.hMusic: return self.hMusic.geturl()
		if (quality == "high" or quality == "medium") and self.mMusic: return self.mMusic.geturl()
		if self.lMusic: return self.lMusic.geturl()
		return self.mp3Url

class SongDetialResult(RemoteResult):
	class songs(model.List): Element = model.RequireModel('SongInfo')

class Song(model.NamedObject):
	class artists(model.List): Element = model.RequireModel('Artist')
	album   = model.RequireModel('Album')
	duration = model.Integer
	@RPCMethod("GET", "api/song/detail", SongDetialResult)
	def details(self):
		return {'id' : self.id, 'ids' : [self.id]}

class SongSearchResult(RemoteResult): 
	class result(model.Dictionary): 
		songCount = model.Integer
		class songs(model.List): Element = model.RequireModel('Song')

		
@RPCFunction("POST", "api/search/get", SongSearchResult)
def search_song(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 1, 'total': True, 'offset': offset, 'limit': limit}

@RPCFunction("POST", "api/search/get", AlbumSearchResult, dumpfile = sys.stdout)
def search_album(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 10, 'total': True, 'offset': offset, 'limit': limit}

@RPCFunction("POST", "api/search/get", ArtistSearchResult)
def search_artist(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 100, 'total': True, 'offset': offset, 'limit': limit}

model.link_model(globals())
if __name__ == "__main__":
	#print search_song(keyword = "black or white").result.songs[0].details().songs[0]["high"]
	print search_song(keyword = "安和桥").result.songs[0].details().songs[0]["high"]	
