from options import getopt
import client
import pycurl
import sys
import cache
import random
class HttpClient(client.Client):
	_nextserver = random.randint(1,2)
	def __init__(self, path, write_func):
		self._host = getopt("Servers")[HttpClient._nextserver]
		self._url =  "%s%s"%(self._host, path)
		self._path = path
		HttpClient._nextserver = 1 - HttpClient._nextserver
		client.Client.__init__(self, path, write_func)
		self._curl = None
		self._cache = cache.getcache()
		self._cache_file = None
	def _initialize_conn(self):
		def on_data_received(data):
			sys.stderr.write("%d\n"%len(data))
			if self._cache_file: 
				self._cache_file.write(data)
			if data: self._chance = getopt("Retry")
			return self._data_receive(data)
		if self._curl: self._curl.close()
		self._curl = pycurl.Curl()
		"""self._curl.setopt(self._curl.HTTPHEADER, [
			'Accept: */*',
			'Accept-Language:z h-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
			'Proxy-Connection: keep-alive',
			'Content-Type: application/x-www-form-urlencoded',
			'Host: %s'%self._host.replace("http://", ""),
			'User-Agent: %s'%getopt("UserAgent")
		])"""
		print self._url
		self._curl.setopt(self._curl.URL, self._url)
		self._curl.setopt(self._curl.WRITEFUNCTION, on_data_received)
		self._curl.setopt(self._curl.TIMEOUT, getopt("Timeout"))
		if getopt("Proxies"): 
			self._curl.setopt(self._curl.PROXY, getopt("Proxies"))
		self._curl.setopt(self._curl.VERBOSE,1)
	def __del__(self):
		if self._curl:
			self._curl.close()
	def perform(self):
		self._initialize_conn()
		if self._current_pos > 0:
			self._curl.setopt(self._curl.RANGE, "%d-"%self._current_pos)
		else:
			self._cache_file = self._cache.open(self._path)
		try:
			self._curl.perform()
		except pycurl.error as e:
			if self._chance > 0: 
				self._chance -= 1
				self.perform()
			else: raise e
		self._cache.close(self._path)		

if __name__ == "__main__":
	h = HttpClient("/VpNWWjzlqL9mvAryWrIfBw==/5708664371463047.mp3", sys.stdout.write)
	h.perform()
