import subprocess
import threading
import sys
import time
class Mpg123:
	STOPPED = 0
	PAUSED  = 1
	PLAYING = 2
	def __init__(self, **kwargs):
		arglist = [kwargs.get('executable', 'mpg123'), '-R'] + kwargs.get('args', [])
		self._proc = subprocess.Popen(arglist, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		self._status = Mpg123.STOPPED
		self._version = ""
		self._title   = ""	
		self._artist  = ""
		self._album   = ""
		self._year    = ""
		self._comment = ""
		self._genre   = ""
		self._resource= ""
		self._srate   = 0 
		self._stereo  = 0
		self._frame_played = 0
		self._frame_left   = 0
		self._time_played = 0
		self._time_left = 0
		self._stopped = False
		self._last_error = ""
		self._volumn = 100
		self._on_status_changed = kwargs.get("on_status_changed", lambda _: None)
		self._on_frame_played   = kwargs.get("on_frame_played", lambda _:None)
		self._on_status_changed = kwargs.get("on_status_changed", lambda _:None)
		self._on_resource_loaded = kwargs.get("on_resource_loaded", lambda _:None)
		self._on_stream_detected = kwargs.get("on_stream_detected", lambda _:None)
		self._on_error           = kwargs.get("on_error", lambda _:None)
		def _update_status():
			while not self._stopped:
				msg = self._proc.stdout.readline().strip()
				msgtype, msgbody= msg[1], msg[3:]
				#if msgtype != 'F': print msg
				if msgtype == 'R':
					self._version = msgbody
				elif msgtype == 'I':
					k,v = msgbody.split(':')
					_,k = k.split('.')
					if k == 'title': self._title = v
					elif k == 'artist': self._artist = v
					elif k == 'album' : self._album = v
					elif k == 'year'  : self._year = v
					elif k == 'comment': self._comment = v
					elif k == 'genre' : self._genre = v
					self._on_resource_loaded(self)
				elif msgtype == 'S':
					v = msgbody.split()
					self._srate, self._stereo = int(v[2]), v[3]
					self._on_stream_detected(self)
				elif msgtype == 'F':
					v = msgbody.split()
					self._frame_played = int(v[0])
					self._frame_left   = int(v[1])
					self._time_played  = float(v[2])
					self._time_left    = float(v[3])
					self._on_frame_played(self)
				elif msgtype == 'P':
					v = msgbody.split()[0]
					self._status = int(v)
					self._on_status_changed(self)	
				elif msgtype == 'E':
					self._last_error = msgbody
				elif msgtype == 'V': 
					self._volumn = float(msgbody[:-1])
		self._thread = threading.Thread(target = _update_status)
		self._thread.daemon = True
		self._thread.start()
	def _send_cmd(self, *cmd):
		self._proc.stdin.write(" ".join(cmd))
		self._proc.stdin.write("\n")
		self._proc.stdin.flush()
	def play(self, url):
		self._send_cmd('l', url)
		self._resource = url
	def toggle_pause(self):
		self._send_cmd('p')
	def stop(self):
		self._send_cmd('s')
	def seek(self, how):
		self._send_cmd('j', how)
	def volumn(self, value): self._send_cmd('v', str(value))	
	def __getitem__(self, key):
		if key == "status":return self._status
		if key == "version": return self._version
		if key == "title" : return self._title
		if key == "artist": return self._artist
		if key == "album" : return self._album
		if key == "year" : return self._year
		if key == "genre" : return self._genre
		if key == "resource": return self._resource
		if key == "sample_rate": return self._srate
		if key == "stereo": return self._stereo
		if key == "frame_played": return self._frame_played
		if key == "frame_left": return self._frame_left
		if key == "time_played": return self._time_played
		if key == "time_left": return self._time_left
		if key == "last_error": return self._last_error
		if key == "volumn": return self._volumn	
		raise KeyError(key)
	def finalize(self):
		self._stopped = True
	def __del__(self):
		if self._proc:
			self._proc.terminate()

if __name__ == "__main__":
	def update_time(what):
		print what['time_played']
	p = Mpg123(on_frame_played = update_time)
	p.play("http://127.0.0.1:8000/KSqKHwTaDrQXHlY52TRwsA==/7704277977980035.mp3")
	sys.stdin.readline()
	print p['version']
	print p['title']
	p.toggle_pause()
	sys.stdin.readline()
	p.toggle_pause()
	sys.stdin.readline()
	p.play("http://127.0.0.1:8000/VpNWWjzlqL9mvAryWrIfBw==/5708664371463047.mp3")
	sys.stdin.readline()
	print p['title']
	p.seek("-10s")
	sys.stdin.readline()
	print p['last_error']	
	p.finalize()
