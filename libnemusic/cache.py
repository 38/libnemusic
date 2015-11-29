import pickle
import os
import hashlib
class CachedItem:
	def __init__(self, timestamp, method, path, request_data, response_data):
		self.timestamp = timestamp
		self.method    = method
		self.path      = path
		self.request   = request_data
		self.content   = response_data
class APICache:
	def __init__(self, cache_dir):
		if not os.path.exists(cache_dir):
			os.mkdir(cache_dir, 0777)
		elif not os.path.isdir(cache_dir):
			raise Exception("The cache root is not a directory")
		self._root = cache_dir
	def _key(self, method, url, data):
		return "%s/%s"%(self._root, hashlib.sha256(repr((method, url, data))).hexdigest())
	def query(self, method, url, request_data):
		key = self._key(method, url, request_data)
		if os.path.exists(key) and not os.path.isdir(key):
			cached_data = pickle.load(file(key))
			if method == cached_data.method and url == cached_data.path and request_data == cached_data.request:
				return cached_data.content
		return None
	def update(self, timestamp, method, url, request_data, response_data):
		key = self._key(method, url, request_data)
		try:
			pickle.dump(CachedItem(timestamp, method, url, request_data, response_data), file(key, "w"), pickle.HIGHEST_PROTOCOL)
			return True
		except:
			return False
