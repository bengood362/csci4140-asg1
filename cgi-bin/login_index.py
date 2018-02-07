#!/usr/bin/python
# login_index.cgi
import cgi
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
    <form action="try_logout.py" method="post" id="auth">
        <input type="hidden" name="username" value="{1}" />
        <input type="submit" value="logout" method="post"/>
    </form>
    <form action="try_change_password.py" method="post" id="auth">
        <input type="submit" value="change_password" method="post"/>
    </form>
    '''.format(cgi.escape(username), cgi.escape(username)))

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
        username = formData.getvalue('username', 'ERROR')
        message = formData.getvalue('message', '')

        htmlTop()

        auth_info(username)
        print "<hr>"
        instagram_feed(5)

        htmlTail()
    except:
        cgi.print_exception()
