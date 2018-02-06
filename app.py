# python_server.py
import sqlite3
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer
import utils
import db_util
OPEN_SHIFT_IP_ADDR = "0.0.0.0"
LOCALHOST_IP_ADDR = "0.0.0.0"
PORT=8080
virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message="hello<br/>hello"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message)
        return

def start_server(ip_addr, port, handler):
    server = HTTPServer((ip_addr, port), handler)
    server.serve_forever()

def main():
    start_server(OPEN_SHIFT_IP_ADDR, PORT, HTTPHandler)
    pass

def debug():
    start_server(LOCALHOST_IP_ADDR, PORT, HTTPHandler)
    pass

if __name__ == "__main__":
    main()
