#!/usr/bin/python
# try_logout.cgi
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

def logoutHTML(success, message):
    if success:
        print('''
        Logout success! now redirecting...<meta http-equiv="refresh" content="0;url=../index.html" />''')
    else:
        print('''Login failed! now redirecting... <meta http-equiv="refresh" content="0;url=login.py?message={0}" />
            '''.format(cgi.escape(message)))

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        username = formData.getvalue('username')
        password = formData.getvalue('password')
        success, message = db_util.logout(username)
        loginHTML(success, message)
        htmlTail()
    except:
        cgi.print_exception()
