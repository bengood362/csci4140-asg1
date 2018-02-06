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

def failedHTMLMid():
    print('''
    <form action="try_login.py" method="post" id="auth">
        username: <input type="text" name="username" required><br>
        password: <input type="password" name="password" required><br>
    </form>
    <button type="submit" form="auth" value="Login">Login</button><br>
    The password is wrong, please try again.''')    

def firstHTMLMid():
    print('''
    <form action="try_login.py" method="post" id="auth">
        username: <input type="text" name="username" required><br>
        password: <input type="password" name="password" required><br>
    </form>
    <button type="submit" form="auth" value="Login">Login</button>''')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        formData = cgi.FieldStorage()
        auth = formData.getvalue('auth')
        htmlTop()
        if auth == "failed":
            failedHTMLMid()
        else:
            firstHTMLMid()
        htmlTail()
    except:
        cgi.print_exception()
