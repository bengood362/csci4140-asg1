#!/usr/bin/python
# try_register.cgi
import cgi
import db_util
import os
import utils

def htmlTop(cookie='', username=''):
    print("Content-type:text/html")
    if cookie != '':
        print("Set-Cookie: cookie={0}".format(cookie))
    if username != '':
        print("Set-Cookie: username={0}".format(username))
    print("\n")
    print("""
        <!DOCTYPE html>
        <html lang='en'>
             <head>
                 <meta charset='utf-8'/>
                 <title>Register</title>
             </head>
         <body>""")

def registerHTML(success, message):
    if success:
        print('''Success! now redirecting...
            <meta http-equiv="refresh" content="0;url=login_index.py?message={0}"/>'''.format(cgi.escape(message)))
    else:
        print('''Failed...now redirecting...
            <meta http-equiv="refresh" content="0;url=register.py?message={0}"/>'''.format(cgi.escape(message)))

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        username = formData.getvalue('username')
        password = formData.getvalue('password')
        password_check = formData.getvalue('password_check')

        if password != password_check:
            htmlTop()
            registerHTML(False, "password_not_match")
            htmlTail()
        else:
            create_success,message=db_util.create_user(username, password)
            if create_success:
                login_success, message=db_util.login_user(username, password)
                cookie_success, cookie=db_util.get_cookie(username)
                htmlTop(cookie, username)
                registerHTML(True, "register and login success")
            else:
                htmlTop()
                registerHTML(False, message)
                htmlTail()

    except:
        cgi.print_exception()
