import os
from options import getopt

class DataCache:
	FILE_CLOSED = 0
	FILE_OPEN   = 1
	def __init__(self, cache_dir):
		if not os.path.exists(cache_dir):
			os.mkdir(cache_dir, 0777)
		elif not os.path.isdir(cache_dir):
			raise Exception("The cache root is not a directory")
		self._root = cache_dir
		self._file_obj_dict = {}
		
	def _key(self, path):
		return "%s/%s"%(self._root, path.split("/")[2][:-4])

	def contains(self, path):
		key = self._key(path)
		if os.path.exists(key) and not os.path.isdir(key):
			return True
		if key in self._file_obj_dict:
			return True
		return False

	def query(self, path):
		key = self._key(path)
		if os.path.exists(key) and not os.path.isdir(key):
			print "[Cache] Open unused " + key + " for read"
			return (DataCache.FILE_CLOSED , file(key, "rb"))
		if key in self._file_obj_dict:
			print "[Cache] Open " + key + " for read"
			return (DataCache.FILE_OPEN, file(key + ".tmp", "rb"))

	def isopenstatus(self, path):
		return self._key(path) in self._file_obj_dict

	def open(self, path):
		key = self._key(path)
		if key in self._file_obj_dict:
			print "[Cache] Cache item " + path + " is already updating"
			return None
		print "[Cache] Opened cache item " + path + " for update"
		temp = key + ".tmp"
		self._file_obj_dict[key] = file(temp, "wb")
		return self._file_obj_dict[key]

	def close(self, path):
		key = self._key(path)
		temp_key = key + ".tmp"
		if key not in self._file_obj_dict: return
		print "[Cache] Finished updating cache item " + path
		fp = self._file_obj_dict[key]
		del self._file_obj_dict[key]
		fp.close()
		os.rename(temp_key, key)
		
	def abort(self, path):
		key = self._key(path)
		temp_key = key + ".tmp"
		if key not in self._file_obj_dict: return
		print "[Cache] Aborted cache item update for" + path
		fp = self._file_obj_dict[key]
		del self._file_obj_dict[key]
		fp.close()
		os.remove(temp_key)	

_cache = None

def getcache():
	global _cache
	if not _cache:
		_cache = DataCache(getopt("CacheDir"))
	return _cache

if __name__ == "__main__":
	print getcache()._key("/VpNWWjzlqL9mvAryWrIfBw==/5708664371463047.mp3")
			
