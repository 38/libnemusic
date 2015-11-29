# -*- coding: utf-8 -*-
import api
#print api.search_song(keyword = "开不了口").result.songs[0].details().songs[0]["high"]
#print api.search_album(keyword = "叶惠美").result.albums[0].details().album.songs[0].artists[0].name

songs = api.search_album(keyword = "叶惠美").result.albums[0].details().album.songs

for song in songs:
	print "http_proxy://115.159.5.247/" + song["low"]
