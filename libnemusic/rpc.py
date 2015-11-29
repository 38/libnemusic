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
		self._dump = dumpfile
		self._cache = use_cache
	
class RPCFunction(RPCBase):
	def __call__(self, modifer):
		def do_rpc_call(**kwargs): return self._what(json.loads(self._how(self._where, modifer(**kwargs), self._dump, self._cache)))
		return do_rpc_call

class RPCMethod(RPCBase):
	def __call__(self, modifer):
		decobj = self
		def do_rpc_call(self, **kwargs): 
			return decobj._what(json.loads(decobj._how(decobj._where, modifer(self, **kwargs), decobj._dump, decobj._cache)))
		return do_rpc_call
	
