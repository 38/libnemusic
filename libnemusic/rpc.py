import model
import network
import json

class RemoteResult(model.Dictionary):
	"""This is the base data model for the RPC result"""
	code = model.String


class RPC:
	"""The remote procedure decorator"""
	session = network.NEMusicSession()
	def __init__(self, how, where, result_model, session = None):
		"""how : "GET" or "POST", where : url, outtype : the result model, session : pass a session object if you need an seperate session"""
		self._how = session[how] if session else RPC.session[how]
		self._where = where
		self._what = result_model
	def __call__(self, modifer):
		def do_rpc_call(**kwargs): return self._what(json.loads(self._how(self._where, modifer(**kwargs)).getvalue()))
		return do_rpc_call

