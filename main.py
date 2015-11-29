# -*- coding: utf-8 -*-
import config
import libnemusic
import client
import sys

#print libnemusic.api.search_song(keyword = "开不了口").result.songs[0].details().songs[0]["high"]
#print libnemusic.api.search_album(keyword = "叶惠美").result.albums[0].details().album.songs[0].artists[0].name


#libnemusic.setopt(**config.config)
#client.setopt(**config.config)


songs = libnemusic.api.search_album(keyword = "叶惠美").result.albums[0].details().album.songs

for song in songs:
	print "http://127.0.0.1:8000" + song.lMusic.getpath()

#client.getclient("/VpNWWjzlqL9mvAryWrIfBw==/5708664371463047.mp3", lambda x: x, lambda x: x)

#print libnemusic.api.search_song(keyword = "風になる").result.songs[0].details(dumpfile = sys.stdout, usecache = False).songs[0].lMusic.getpath()
