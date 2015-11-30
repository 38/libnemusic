#This is the config file for the entire library
#TODO load the configurations from external file

#This is the hard coded config file
_config_table = { 
	"RSAModulus" : 0x00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7, 
	"RSAPubKey" : 0x10001, 
	"AESNonce" : "0CoJUm6Qyw8W8jud", 
	"XorKey" : "3go8&$8*3*3h0k(2)2", 
	"BaseURL" : "http://music.163.com/", 
	"CookiePath" : "/tmp/nemusic.cookies", 
	"UserAgent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0",
	"Proxies"   : None,
	"Timeout"   : 15,
	"Retry"     : 3,
	"EnableCache" : True,
	"CacheDir":  "/tmp/nemusic_cache"
}

def setopt(config_table):
	for k,v in _config_table.items():
		_config_table[k] = config_table.get(k, v)

def getopt(key, required = False):
	if required : return _config_table[key]
	return _config_table.get(key, None)
