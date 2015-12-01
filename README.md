# libnemusic
==
Example

$ python
Python 2.7.3 (default, Jun 22 2015, 19:33:41) 
	[GCC 4.6.3] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import server
	>>> import libnemusic
	>>> import player
	>>> album = libnemusic.api.search_album(keyword = "范特西").get_albums().next()
	>>> songs = album.get_songs()
	>>> pl = player.playlist.Playlist()
	>>> for s in songs: pl.append(s.name, s.artists[0].name, s.lMusic.playTime, "http://localhost:8000" + s.lMusic.getpath())
	... 
	>>> service = server.Service(file("/tmp/nemusic.log", "w", 0))
	>>> pl.play()

