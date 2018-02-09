#!/usr/bin/python
# try_logout.cgi
import cgi
import db_util
import utils
import os

def htmlTop():
    print("Content-type:text/html")
    print("Set-Cookie: cookie=None")
    print("Set-Cookie: username=None\n\n")
    print("""
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Logout</title>
            </head>
        <body>""")

def logoutHTML(success, message):
    if success:
        print('''
        Logout success! now redirecting...<meta http-equiv="refresh" content="0;url=login_index.py" />''')
    else:
        print('''Logout failed! now redirecting... <meta http-equiv="refresh" content="0;url=login.py?message={0}" />
            '''.format(cgi.escape(message)))

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        cookies = utils.get_client_cookie()
        username = cookies.get('username', 'ERROR')
        password = formData.getvalue('password')
        success, message = db_util.logout(username)
        logoutHTML(success, message)
        htmlTail()
    except:
        cgi.print_exception()
