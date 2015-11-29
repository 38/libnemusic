# -*- coding: utf-8 -*-
import api
print api.search_song(keyword = "安和桥").result.songs[0].details().songs[0]["high"]	
