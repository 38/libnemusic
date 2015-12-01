# -*- coding: utf-8 -*-
import config
import libnemusic
import client
import sys
import subprocess
import player
from server import Service

service = Service(file("/tmp/nemusic_server.log", "w", 0))

pl = player.playlist.Playlist()

#for song in libnemusic.api.search_album(keyword = "七里香").result.albums[0].details().album.songs:
#	pl.append(song.name, song.artists[0].name, 0, "http://localhost:8000" + song.mMusic.getpath())
#libnemusic.api.search_album(keyword = "七里香").result.albums[0].details(dumpfile = sys.stderr)
#for song in libnemusic.api.search_album(keyword = "八度空间").result.albums[0].get_songs():
#	pl.append(song.name, song.artists[0].name, song.lMusic.playTime, "http://localhost:8000" + song.lMusic.getpath())
#song = libnemusic.api.search_song(keyword = "I'm yours").get_songs().next().info()
#pl.append(song.name, song.artists[0].name, song.lMusic.playTime, "http://localhost:8000" + song.lMusic.getpath())
#pl.play()

sg = libnemusic.api.search_album(keyword
