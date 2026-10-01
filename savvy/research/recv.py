import http.server, json, sys
class H(http.server.BaseHTTPRequestHandler):
    def _c(self):
        self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Headers','*'); self.send_header('Access-Control-Allow-Methods','POST,OPTIONS')
    def do_OPTIONS(self):
        self.send_response(204); self._c(); self.end_headers()
    def do_POST(self):
        n=int(self.headers.get('Content-Length',0)); b=self.rfile.read(n)
        name=self.path.strip('/') or 'out'
        open(name+'.json','wb').write(b)
        self.send_response(200); self._c(); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self,*a): pass
http.server.HTTPServer(('127.0.0.1',8765),H).serve_forever()
