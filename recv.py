import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers.get('Content-Length',0)); data=self.rfile.read(n)
        name=self.path.strip('/') or 'dump'
        open(f'C:/cca/{name}.txt','ab').write(data+b'\n')
        self.send_response(200); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers(); self.wfile.write(b'ok')
    def do_OPTIONS(self):
        self.send_response(200); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Headers','*'); self.end_headers()
    def log_message(self,*a): pass
http.server.HTTPServer(('127.0.0.1',8765),H).serve_forever()
