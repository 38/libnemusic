import client
import httpclient
import cacheclient
import cache
def getclient(path, write_func, header_func):
	if cache.getcache().contains(path):
		return cacheclient.CacheClient(path, write_func, header_func)
	else:
		return httpclient.HttpClient(path, write_func, header_func)
