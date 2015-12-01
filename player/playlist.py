import mpg123
import pickle
import sys
import libnemusic
class PlaylistItem:
	def __init__(self, disp_name, artist, duration, url):
		self.disp_name = disp_name
		self.artist    = artist
		self.duration  = duration
		self.url       = url
	def play(self, player):
		player.play(self.url)
	def __str__(self):
		return self.artist + " - " +  self.disp_name
class Playlist(list):
	PLAYING = 0
	STOPPED = 1
	def _get_next(self):
		if len(self) - 1 == self._current: 
			if self.loop: return 0
			else: return -1
		else: return self._current + 1
	def __init__(self, **kwargs):
		self._current = 0
		self._state   = self.STOPPED
		self.loop    = False
		self._player  = None #mpg123.Mpg123(on_status_changed = on_status_changed)
		self._player_cb = kwargs
		self._sc_handler = lambda _: None
		list.__init__(self)
	def __delitem__(self, idx):
		if self._current == idx:
			list.__delitem__(self, idx)
			if self._state == self.PLAYING: 
				self.play()
		elif self._current > idx:
			self._current -= 1
			list.__delitem__(self, idx)
		else:
			list.__delitem__(self, idx)
	def play(self, begin = None):
		def on_status_changed(player):
			if player['status'] == player.STOPPED:
				if self._state == self.PLAYING:
					self.play(self._get_next())
			self._sc_handler(player)
		if begin != None:
			if begin < 0: 
				self._state = self.STOPPED
				return
			self._current = begin
		self._state = self.PLAYING
		if not self._player:
			if "on_status_changed" in self._player_cb:
				self._sc_handler = self._player_cb["on_status_changed"]
				del self._player_cb["on_status_changed"]
			self._player = mpg123.Mpg123(on_status_changed = on_status_changed, **self._player_cb)
		self[self._current].play(self._player)
	def toggle_pause(self, begin = None): 
		if self._state == self.PLAYING: self._player.toggle_pause()
	def stop(self):
		if self._state == self.PLAYING: 
			self._state = self.STOPPED
			self._player.stop()
	def skip(self, forward = True):
		if self._state == self.PLAYING:
			if forward: self._player.stop()	
			elif not self.loop: self.play(max(self._current - 1, 0))
			else: self.play((len(self) - 1 + self._current) % len(self))
	def append(self, disp_name, artist, duration, url):
		list.append(self, PlaylistItem(disp_name, artist, duration, url))
	def __getitem__(self, key):
		if isinstance(key, str):	
			return self._player[key]
		return list.__getitem__(self, key)
	def volumn(self, value):
		self._player.volumn(value)
	def save(self, fout):
		pickle.dump([item for item in self], fout, pickle.HIGHEST_PROTOCOL)
	def load(self, fin):
		for item in pickle.load(fin): list.append(self, item)
