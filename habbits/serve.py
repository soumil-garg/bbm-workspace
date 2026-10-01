from http.server import BaseHTTPRequestHandler,HTTPServer
import os,urllib.parse
class H(BaseHTTPRequestHandler):
    def _h(self):
        self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Headers','*');self.send_header('Access-Control-Allow-Private-Network','true');self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
    def do_OPTIONS(self): self.send_response(204);self._h();self.end_headers()
    def do_GET(self):
        n=urllib.parse.unquote(self.path.strip('/'))
        b=open(f'C:/cca/habbits/p3/{n}.txt','rb').read()
        self.send_response(200);self._h();self.send_header('Content-Type','text/plain; charset=utf-8');self.end_headers();self.wfile.write(b)
    def do_POST(self):
        n=self.path.strip('/'); b=self.rfile.read(int(self.headers['Content-Length']))
        open(f'C:/cca/habbits/{n}','wb').write(b); self.send_response(200);self._h();self.end_headers();self.wfile.write(b'ok')
    def log_message(self,*a): pass
HTTPServer(('127.0.0.1',8765),H).serve_forever()
