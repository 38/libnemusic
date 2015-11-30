from options import getopt
import client
import cache
import sys
import os
import time
class CacheClient(client.Client):
	def __init__(self, path, write_func, header_func):
		self._cache = cache.getcache()
		self._cache_mode, self._cache_file = self._cache.query(path)
		self._write_func = write_func
		self._header_func =  header_func
	def __del__(self):
		if self._cache_file:
			self._cache_file.close()
	def perform(self):
		block_size = getopt("BlockSize")
		self._header_func("Content-Type:  audio/mpeg\n")
		self._header_func("Content-Length: %d\n"%os.fstat(self._cache_file.fileno()).st_size)
		self._header_func("NE-Client-Type: Cached\n")
		if not block_size: block_size = 1024
		while True:
			next_block = self._cache_file.read(block_size)
			if not next_block:
				if self._cache_mode == self._cache.FILE_OPEN and self.isopenstatus(path): time.sleep(0.1)
				else: break
			self._write_func(next_block)
		self._cache_file.close()

