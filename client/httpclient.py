from options import getopt
import client
import pycurl
import sys
import cache
import random
import traceback
class HttpClient(client.Client):
	_nextserver = random.randint(0,1)
	def __init__(self, path, write_func, header_func):
		self._host = getopt("Servers")[HttpClient._nextserver]
		self._url =  "%s%s"%(self._host, path)
		self._path = path
		HttpClient._nextserver = 1 - HttpClient._nextserver
		client.Client.__init__(self, path, write_func)
		self._curl = None
		self._cache = cache.getcache()
		self._cache_file = None
		self._header_func = header_func
		self._chance = 0
	def _initialize_conn(self):
		def on_data_received(data):
			if self._cache_file: 
				self._cache_file.write(data)
			if data: self._chance = getopt("Retry")
			try:
				return self._data_receive(data)
			except Exception as e:
				traceback.print_exc(e)
		if self._curl: self._curl.close()
		self._curl = pycurl.Curl()
		self._curl.setopt(self._curl.HTTPHEADER, [
			'Accept: */*',
			'Accept-Language:z h-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
			'Proxy-Connection: keep-alive',
			'Content-Type: application/x-www-form-urlencoded',
			'Host: %s'%self._host.replace("http://", ""),
			'User-Agent: %s'%getopt("UserAgent")
		])
		self._curl.setopt(self._curl.URL, self._url)
		self._curl.setopt(self._curl.WRITEFUNCTION, on_data_received)
		self._curl.setopt(self._curl.TIMEOUT, getopt("Timeout"))
		self._curl.setopt(self._curl.FOLLOWLOCATION, 1)
		if getopt("Proxies"): 
			self._curl.setopt(self._curl.PROXY, getopt("Proxies"))
	def __del__(self):
		if self._curl:
			self._curl.close()
	def perform(self):
		self._initialize_conn()
		if self._current_pos > 0:
			self._curl.setopt(self._curl.RANGE, "%d-"%self._current_pos)
		else:
			self._cache_file = self._cache.open(self._path)
			self._curl.setopt(self._curl.HEADERFUNCTION, self._header_func)
		try:
			self._curl.perform()
		except pycurl.error as e:
			if self._chance > 0:
				print >> sys.stderr, "[HttpClient] Read failure: %s, take another chance from offset %d (chances left : %d)" % (e, self._current_pos ,self._chance)
				self._chance -= 1
				self.perform()
			else:
				print >> sys.stderr, "[HttpClient] No more chance for this connection at %d, give up (exception = %s)" % (self._current_pos, e)				
				self._cache.abort(self._path)	
				raise e	
		self._cache.close(self._path)		
