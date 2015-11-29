import model
import network
import json

class RemoteResult(model.Dictionary):
	"""This is the base data model for the RPC result"""
	code = model.String

class RPCBase:
	"""The remote procedure decorator"""
	session = network.NEMusicSession()
	def __init__(self, how, where, result_model, session = None, dumpfile = None, use_cache = True):
		"""how : "GET" or "POST", 
		   where : url, 
		   outtype : the result model, 
		   session : pass a session object if you need an seperate session
		   no_cache: force the RPC do not use cache"""
		self._how = session[how] if session else RPCBase.session[how]
		self._where = where
		self._what = result_model
		self._opts = {'dumpfile': dumpfile, 'usecache': use_cache}
	def _getopt(self, key, kwargs):
		ret = self._opts[key]
		if key in kwargs: 
			ret = kwargs[key]
			del kwargs[key]
		return ret
class RPCFunction(RPCBase):
	def __call__(self, modifer):
		def do_rpc_call(**kwargs): 
			dump  = self._getopt("dumpfile", kwargs)
			cache = self._getopt("usecache", kwargs)
			return self._what(json.loads(self._how(self._where, modifer(**kwargs), dump, cache)))
		return do_rpc_call

class RPCMethod(RPCBase):
	def __call__(self, modifer):
		decobj = self
		def do_rpc_call(self, **kwargs): 
			dump  = decobj._getopt("dumpfile", kwargs)
			cache = decobj._getopt("usecache", kwargs)
			return decobj._what(json.loads(decobj._how(decobj._where, modifer(self, **kwargs), dump, cache)))
		return do_rpc_call
	
