#!/usr/bin/env python
import BaseHTTPServer
import client
import traceback
import SocketServer

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		path = self.path
		self.headerbuf = ""
		self.headerwritten = False
		def _header(data):
			self.headerbuf += data
			if '\n' in self.headerbuf:
				headers = self.headerbuf.split('\n')
				for header in headers[:-1]:
					if ':' not in header: continue
					idx = header.index(':')
					k,v = header[:idx].strip(), header[idx + 1:].strip()
					if k == "Accept-Ranges": continue
					self.send_header(k, v)
				self.headerbuf = headers[-1]
			self.send_header('Connection', 'close')
		def _content(data):
			if not self.headerwritten:
				self.end_headers()
				self.headerwritten = True
			self.wfile.write(data)
		try:
			print self.headers
			if len(path.split('/')) == 3:
				c = client.getclient(path, _content, _header)
				self.send_response(200)
				c.perform()
				self.wfile.close()
			else:
				self.send_response(404)
				self.send_header("Content-Type", "text/html")
				self.end_headers()
				self.wfile.write("<html><body>HTTP 404 - Not Found</body></html>")
		except Exception as e:
			traceback.print_exc(e)
			self.send_response(500)
			self.send_header("Content-Type", "text/html")
			self.end_headers()
			self.wfile.write("<html> <body>HTTP 500 - Server Internal Error <br> %s </body> </html>" % e)
			
class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass

if __name__ == "__main__":
	server_class = ThreadedHTTPServer
	httpd = server_class(("127.0.0.1", 8000), ServerHandler)
	httpd.serve_forever()
