# python_server.py
import sqlite3
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer
import utils
OPEN_SHIFT_IP_ADDR = "172.30.69.5"
LOCALHOST_IP_ADDR = "0.0.0.0"

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

def init_db():
    print_("starting init db")
    user_conn = sqlite3.connect('user.db')
    user_c = conn.cursor()
    # c.execute('''CREATE TABLE user
    #          (date text, trans text, symbol text, qty real, price real)''')

def main():
    start_server(OPEN_SHIFT_IP_ADDR, 5003, HTTPHandler)
    pass

def debug():
    start_server(LOCALHOST_IP_ADDR, 5003, HTTPHandler)
    pass

if __name__ == "__main__":
    main()
