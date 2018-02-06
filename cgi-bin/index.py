#!/usr/bin/python

import cgi
def htmlTop():
    print("""Content-type:text/html\n\n
             <!DOCTYPE html>
             <html lang='en'>
                 <head>
                     <meta charset='utf-8'/>
                     <title>Web Instagram</title>
                 </head>
                 <body>""")

def htmlMid():
    print('''<form method="post" action="login.py">
    <input type="submit" value="Login" method="post"/></form>
    <br>
    <form method="post" action="register.py">
    <input type="submit" value="Register" method="post"/></form>
        ''')

def htmlTail():
    print("""</body>
            </html>""")

if __name__ == '__main__':
    try:
        htmlTop()
        htmlMid()
        htmlTail()
    except:
        cgi.print_exception()
