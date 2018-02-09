#!/usr/bin/python
# index.cgi
import db_util
import utils
import os
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
    print("<h1>Start! Login or register web instagram today!</h1>")

def loginMid():
    print('''Logging in with cookie! now redirecting... <meta http-equiv="refresh" content="0;url=login_index.py" />
    ''')

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
        cookies = utils.get_client_cookie()
        if cookies.get('cookie'):
            auth_cookie = cookies['cookie']
            auth_success, message=db_util.get_username(auth_cookie)
            if auth_success:
                username = message
                loginMid()
            else:
                # htmlMid()
                # Disabled it because non-user should be able to view photo too
                loginMid()
        else:
            htmlMid()
        htmlTail()
    except:
        cgi.print_exception()
