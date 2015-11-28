import network
from rpc import RemoteResult, RPC
import model

class Artist(model.NamedObject): 
	pass

class Album(model.NamedObject):
	artist = Artist
	
class Song(model.NamedObject):
	class artists(model.List): Element = Artist
	album   = Album
	duration = model.Integer
	@RPC("GET", "api/song/detail", RemoteResult)
	def details(self):
		return {'id' : self.id, 'ids' : [self.id]}

class SongSearchResult(RemoteResult): 
	class result(model.Dictionary): 
		songCount = model.Integer
		class songs(model.List): Element = Song

class AlbumSearchResult(RemoteResult):
	class result(model.Dictionary):
		albumCount = model.Integer
		class albums(model.List): Element = Album
		
class ArtistSearchResult(RemoteResult):
	class result(model.Dictionary):
		artistCount = model.Integer
		class artists(model.List): Element = Album
		
@RPC("POST", "api/search/get", SongSearchResult)
def search_song(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 1, 'total': True, 'offset': offset, 'limit': limit}

@RPC("POST", "api/search/get", AlbumSearchResult)
def search_album(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 10, 'total': True, 'offset': offset, 'limit': limit}

@RPC("POST", "api/search/get", ArtistSearchResult)
def search_artist(keyword, offset = 0, limit = 60):
	return {'s': keyword, 'type': 100, 'total': True, 'offset': offset, 'limit': limit}

if __name__ == "__main__":
	print search_song(keyword = "black or white").result.songs[0]
