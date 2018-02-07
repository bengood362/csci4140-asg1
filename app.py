# python_server.py
import sqlite3
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from CGIHTTPServer import CGIHTTPRequestHandler
import SocketServer
import os
OPEN_SHIFT_IP_ADDR = "0.0.0.0"
LOCALHOST_IP_ADDR = "0.0.0.0"
PORT=8080
virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
index_script = 'index.py'

#NOTE: ABANDONED
class CGIWithRedirectRH(CGIHTTPRequestHandler):
    pass


def start_server(ip_addr, port, handler):
    server = HTTPServer((ip_addr, port), handler)
    print "start serving at {0}:{1}".format(OPEN_SHIFT_IP_ADDR, PORT)
    server.serve_forever()

def main():
    start_server(OPEN_SHIFT_IP_ADDR, PORT, CGIHTTPRequestHandler)
    pass

def debug():
    start_server(LOCALHOST_IP_ADDR, PORT, CGIHTTPRequestHandler)
    pass

if __name__ == "__main__":
    main()
