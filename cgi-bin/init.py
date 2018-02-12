#!/usr/bin/python
# init.cgi
import cgi
import db_util
import utils
def htmlTop():
    print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang='en'>
             <head>
                 <meta charset='utf-8'/>
                 <title>Login</title>
             </head>
         <body>""")

def startInitHTML(message=''):
    print('''<h1>System initialization</h1>
        Important: All data will be deleted.<br>
        <form action="clean.py" method="get">
            <button type="submit" value="Please go ahead." />Please go ahead.</button>
        </form>
        <form action="../index.html" method="get">
            <button type="submit" value="Go home" />Go home</button>
        </form>''')

    if message != '':
        print "<br>"+cgi.escape(message)

def adminFormHTML(message=''):
    print('''<h1>Login</h1>
    <form action="init.py" method="post" id="auth">
        Login admin account
        password: <input type="password" name="password" required><br><br>
    </form>
    <button type="submit" form="auth" value="Login">Login</button>''')

    if message != '':
        print "<br>"+cgi.escape(message)

def registerAdminAccountHTML(message=''):
    print('''<h1>Login</h1>
    <form action="init.py" method="post" id="auth">
        Change admin default password because first enter this page<br>
        password: <input type="password" name="password" required><br><br>
        retype password: <input type="password" name="password_check" required><br><br>
    </form>
    <button type="submit" form="auth" value="Login">Login</button>''')

    if message != '':
        print "<br>"+cgi.escape(message)

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        password = formData.getvalue("password")
        password_check = formData.getvalue("password_check")

        if db_util.admin_exist():
            if password:
                success, message = db_util.login_admin(password)
            else:
                success = False
                message = "Please login"
            if success:
                startInitHTML(message)
            else:
                adminFormHTML(message)
        else:
            if password == None and password_check == None: #start
                registerAdminAccountHTML()
            elif (password != password_check) or password == None:
                registerAdminAccountHTML("wrong password for password check")
            else:
                success, message = db_util.create_admin(password)
                startInitHTML(message)

        htmlTail()
    except:
        cgi.print_exception()
