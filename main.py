# -*- coding: utf-8 -*-
import config
import libnemusic
import client
import sys
import subprocess
import player

class Service:
	def __init__(self, server_log):
		self._service_proc = subprocess.Popen(["./server.py"], stdout = server_log, stderr = server_log)
	def __del__(self):
		if self._service_proc: 
			self._service_proc.terminate()

service = Service(file("/tmp/nemusic_server.log", "w"))
#url = "http://localhost:8080" + libnemusic.api.search_song(keyword = "明天,你好").result.songs[0].details().songs[0].mMusic.getpath()
#print url
#m = subprocess.Popen(["mpg123", "-R"], stdin = subprocess.PIPE)

pl = player.playlist.Playlist()

for song in libnemusic.api.search_album(keyword = "七里香").result.albums[0].details().album.songs:
	pl.append(song.name, song.artists[0].name, 0, "http://localhost:8000" + song.mMusic.getpath())
