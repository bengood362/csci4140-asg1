#!/usr/bin/python
# try_login.cgi
import cgi
import db_util
import utils

def htmlTop(cookie, username):
    if cookie != '':
        print("Set-Cookie: cookie={0}".format(cookie))
        print("Set-Cookie: username={0}".format(username))
    print("Content-type:text/html\n")
    print("""
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Login</title>
            </head>
        <body>""")

def loginHTML(success, message):
    if success:
        print('''
        Login success! now redirecting...<meta http-equiv="refresh" content="0;url=login_index.py" />''')
    else:
        print('''Login failed! now redirecting... <meta http-equiv="refresh" content="0;url=login.py?message={0}" />
            '''.format(cgi.escape(message)))

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        username = formData.getvalue('username')
        password = formData.getvalue('password')
        login_succ, message = db_util.login_user(username, password)
        if login_succ:
            cookie_succ,cookie=db_util.get_cookie(username)
        else:
            cookie=''
        htmlTop(cookie, username)
        loginHTML(login_succ, message)
        htmlTail()
    except:
        cgi.print_exception()
