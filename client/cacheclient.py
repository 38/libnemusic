from options import getopt
import client
import cache
import sys

class CacheClient(client.Client):
	def __init__(self, path, write_func):
		self._cache = cache.getcache()
		self._cache_file = self._cache.query(path)
		self._write_func = write_func
	def __del__(self):
		if self._cache_file:
			self._cache_file.close()
	def perform(self):
		block_size = getopt("BlockSize")
		if not block_size: block_size = 65536
		while True:
			next_block = self._cache_file.read(block_size)
			if not next_block: break
			self._write_func(next_block)
		self._cache_file.close()

