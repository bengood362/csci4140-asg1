#!/usr/bin/python
# try_change_password.cgi
import cgi
import utils
def htmlTop():
    print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang='en'>
             <head>
                 <meta charset='utf-8'/>
                 <title>Change password</title>
             </head>
         <body>""")

def htmlMid(username, message=''):
    print('''<h1>Change password</h1>
    <form action="try_change_password.py" method="post" id="change">
        <input type="hidden" name="username" value="{0}"/>
        original password: <input type="password" name="password_o" required><br>
        new password: <input type="password" name="password_n" required><br>
        retype new password: <input type="password" name="password_n2" required><br><br>
    </form>
    <button type="submit" form="change" value="Change password">Change password</button>
    <form action="login_index.py" method="get">
        <input type="hidden" name="username" value="{0}"/>
        <input type="submit" value="Discard change"/>
    </form>'''.format(username))
    if message != '':
        print "<br>"+message

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        message = formData.getvalue('message','')
        username = formData.getvalue('username','ERROR')
        htmlTop()
        htmlMid(username,message)
        htmlTail()
    except:
        cgi.print_exception()
