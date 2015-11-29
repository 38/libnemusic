from options import getopt
import random
import cache
class Client:
	def __init__(self, path ,write_func):
		self._write_func = write_func
		self._path = path
		self._current_pos = 0
	def _data_receive(self, data):
		self._current_pos += len(data)
		self._write_func(data)
	def perform(self):
		raise Expcetion("Method Unimpelemented")

