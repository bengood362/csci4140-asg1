# python_server.py
import sqlite3
import SimpleHTTPServer
import SocketServer
import utils

def init_db():
    print_("starting init db")
    user_conn = sqlite3.connect('user.db')
    user_c = conn.cursor()
    # c.execute('''CREATE TABLE user
    #          (date text, trans text, symbol text, qty real, price real)''')

def main():
    pass

def debug():
    pass

if __name__ == "__main__":
    main()
    print "testing"
