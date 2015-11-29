import config
import pycurl
from cookielib import LWPCookieJar
import urllib
import sys
from StringIO import StringIO
import cache
class NEMusicSession:
	_base_url = config.get_config("BaseURL")
	_proxies  = config.get_config("Proxies") 
	_cookies  = config.get_config("CookiePath")
	_timeout  = config.get_config("Timeout")
	_retry    = config.get_config("Retry")
	_cache    = config.get_config("EnableCache")
	_cache_object = None
	_headers  = [
            'Accept:*/*',
            'Accept-Language:zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection:keep-alive',
            'Content-Type:application/x-www-form-urlencoded',
            'Host:music.163.com',
            'Referer:http://music.163.com/search/',
			'User-Agent:' + config.get_config("UserAgent")
	]
	def __init__(self):
		self._base_url = NEMusicSession._base_url
		if self._cache and not self._cache_object:
			self._cache_object = cache.APICache(config.get_config("CacheDir"))

	def _query_cache(self, method, path, request_data):
		if self._cache_object:
			return self._cache_object.query(method, path, request_data)
		return None

	def _update_cache(self, method, path, request_data, response_data):
		if self._cache_object: 
			return self._cache_object.update(0, method, path, request_data, response_data) #TODO add the timestamp
		return False

	def _initialize_request(self, url):
		buffer = StringIO()
		self._curl = pycurl.Curl()
		self._curl.setopt(self._curl.HTTPHEADER, NEMusicSession._headers)
		if NEMusicSession._proxies: self._curl.setopt(self._curl.PROXY, NEMusicSession._proxies)
		self._curl.setopt(self._curl.COOKIEFILE, NEMusicSession._cookies)
		self._curl.setopt(self._curl.COOKIEJAR, NEMusicSession._cookies + ".incoming")
		self._curl.setopt(self._curl.URL, url)
		self._curl.setopt(self._curl.WRITEFUNCTION, buffer.write)
		self._curl.setopt(self._curl.TIMEOUT, NEMusicSession._timeout)
		self._curl.setopt(self._curl.HEADERFUNCTION, sys.stdout.write)
		return buffer
	
	def _do_request(self, method, path, data, dumpfile, use_cache):
		if "__suffix__" in data: 
			path = path + str(data["__suffix__"])
			del data["__suffix__"]
		if use_cache:
			cached = self._query_cache(method, path, data)
			if cached: return cached
		if method == "GET":
			if data: 
				url = "".join([self._base_url, path, "?", urllib.urlencode(data)])
			else:
				url = "".join([self._base_url, path])
		elif method == "POST":
			url = "".join([self._base_url, path])
		last_exception = None
		for i in xrange(NEMusicSession._retry):
			try:
				buffer = self._initialize_request(url)
				if method == "POST": self._curl.setopt(self._curl.POSTFIELDS, urllib.urlencode(data))
				self._curl.perform()
				self._curl.close()
				self._update_cache(method, path, data, buffer.getvalue())
				if dumpfile: 
					dumpfile.write("==> %s %s\n<== " % (method,url))
					dumpfile.write(buffer.getvalue())
					dumpfile.write("\n")
				return buffer.getvalue()
			except Exception as e:
				last_exception = e
		raise last_exception	
	def do_GET(self, path, data, dumpfile, use_cache): return self._do_request("GET", path, data, dumpfile, use_cache)	
	def do_POST(self, path, data, dumpfile, use_cache): return self._do_request("POST", path, data, dumpfile, use_cache)
	def __getitem__(self, method):
		if method == "GET":    return self.do_GET
		elif method == "POST": return self.do_POST
		return None
