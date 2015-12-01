_options = {
		"Servers"  : ["http://m1.music.126.net", "http://m2.music.126.net"],
		"Proxies"  : "115.159.5.247:80",
		"UserAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0",
		"Timeout"  : 15,
		"CacheDir" : "/tmp/nemusic_datacache",
		"Retry"    : 10
}

def setopt(kwargs):
	for k,v in kwargs.items():
		_options[k] = v

def getopt(key, required = False):
	if not required: return _options.get(key, None)
	return _options[key]
