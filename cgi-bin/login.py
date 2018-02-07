#!/usr/bin/python
# login.cgi
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

def htmlMid(message=''):
    print('''
    <form action="try_login.py" method="post" id="auth">
        username: <input type="text" name="username" required><br>
        password: <input type="password" name="password" required><br>
    </form>
    <button type="submit" form="auth" value="Login">Login</button>
    <form action="register.py" method="get">
        <input type="submit" value="Register" method="post"/>
    </form>''')
    if message != '':
        print "<br>"+cgi.escape(message)

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        message = formData.getvalue('message','')
        htmlTop()
        if message == "wrong_password":
            htmlMid("No such account or the password is wrong, please try again.")
        elif message == "register_success":
            htmlMid("Registration success, please login.")
        else:
            htmlMid(message)
        htmlTail()
    except:
        cgi.print_exception()
