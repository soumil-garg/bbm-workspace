from http.server import BaseHTTPRequestHandler,HTTPServer
class H(BaseHTTPRequestHandler):
    def _h(self):
        self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Headers','*');self.send_header('Access-Control-Allow-Private-Network','true');self.send_header('Access-Control-Allow-Methods','POST,OPTIONS')
    def do_OPTIONS(self): self.send_response(204);self._h();self.end_headers()
    def do_POST(self):
        n=self.path.strip('/') or 'data'; b=self.rfile.read(int(self.headers['Content-Length']))
        open(f'C:/cca/habbits/research/{n}.json','wb').write(b); self.send_response(200);self._h();self.end_headers();self.wfile.write(b'ok')
HTTPServer(('127.0.0.1',8765),H).serve_forever()
