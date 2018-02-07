#!/usr/bin/python
import db_util
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

def loginMid(username):
    print('''Logging in with cookie! now redirecting... <meta http-equiv="refresh" content="0;url=login_index.py?username={0}" />
    '''.format(username))

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

def get_cookie():
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        cookies = cookies.split('; ')
        for cookie in cookies:
            cookie_key, cookie_val = cookie.split('=')
            print cookie_val
            if cookie_key == "cookie":
                auth_cookie = cookie_val
                return auth_cookie[1:-1]

if __name__ == '__main__':
    try:
        htmlTop()
        auth_cookie = get_cookie()
        if auth_cookie:
            auth_success, message=db_util.get_username(auth_cookie)
            print(message)
            if auth_success:
                username=message
                loginMid(username)
            else:
                htmlMid()
        else:
            htmlMid()
        htmlTail()
    except:
        cgi.print_exception()
