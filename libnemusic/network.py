import config
import pycurl
from cookielib import LWPCookieJar
import urllib
import sys
from StringIO import StringIO
class NEMusicSession:
	_base_url = config.get_config("BaseURL")
	_proxies  = config.get_config("Proxies") 
	_cookies  = config.get_config("CookiePath")
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

	def _initialize_request(self, url):
		buffer = StringIO()
		self._curl = pycurl.Curl()
		self._curl.setopt(self._curl.HTTPHEADER, NEMusicSession._headers)
		if NEMusicSession._proxies: self._curl.setopt(self._curl.PROXY, NEMusicSession._proxies)
		self._curl.setopt(self._curl.COOKIEFILE, NEMusicSession._cookies)
		self._curl.setopt(self._curl.COOKIEJAR, NEMusicSession._cookies + ".incoming")
		self._curl.setopt(self._curl.URL, url)
		self._curl.setopt(self._curl.WRITEFUNCTION, buffer.write)
		return buffer
		
	def do_GET(self, path, data):
		url = "".join([self._base_url, path, "?", urllib.urlencode(data)])
		buffer = self._initialize_request(url)
		self._curl.perform()
		return buffer
	
	def do_POST(self, path, data):
		url = "".join([self._base_url, path])
		buffer = self._initialize_request(url)
		self._curl.setopt(self._curl.POSTFIELDS, urllib.urlencode(data))
		self._curl.perform()
		print buffer.getvalue()
		return buffer

	def __getitem__(self, method):
		if method == "GET":    return self.do_GET
		elif method == "POST": return self.do_POST
		return None
