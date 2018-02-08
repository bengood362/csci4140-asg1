#!/usr/bin/python
# login_index.cgi
import cgi
import utils
import os
import db_util
def htmlTop():
    print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Login</title>
            </head>
        <body>""")

def auth_info(username):
    print('''username: {0}<br>
    <form action="try_logout.py" method="post" id="logout">
        <input type="hidden" name="username" value="{0}" />
        <input type="submit" value="logout" method="post"/>
    </form>
    <form action="change_password.py" method="post" id="change">
        <input type="hidden" name="username" value="{0}" />
        <input type="submit" value="change_password" method="post"/>
    </form>
    '''.format(cgi.escape(username)))

def upload_image():
    print('''<form action="upload_image.py" method="post">
    <input type="file" name="image"/>
    </form>
    ''')

def instagram_feed(limit=10):
    for i in range(limit):
        print('''instagram_feed''')
        print('<br>')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        cookies = utils.get_client_cookie()
        username = cookies.get('username',"ERROR")
        message = formData.getvalue('message', '')

        htmlTop()

        auth_info(username)
        print "<hr>"

        print "<hr>"
        instagram_feed(5)

        htmlTail()
    except:
        cgi.print_exception()
