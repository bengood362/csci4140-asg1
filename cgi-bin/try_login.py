#!/usr/bin/python
# try_login.cgi
import cgi
import db_util

def htmlTop():
    print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Try logging in...</title>
            </head>
        <body>""")

def successLoginHTML():
    print('''
    redirecting...''')

def unsuccessLoginHTML():
    print('''
    redirecting...
    <meta http-equiv="refresh" content="0;url=login.py?auth=failed" />
    ''')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()
        formData = cgi.FieldStorage()
        username = formData.getvalue('username')
        password = formData.getvalue('password')
        success = db_util.login_user(username, password)
        if success:
            successLoginHTML()
        else:
            unsuccessLoginHTML()
        htmlTail()
    except:
        cgi.print_exception()
