#!/usr/bin/python
# try_register.cgi
import cgi
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

def registerHTML(success, message):
    if success:
        print('''Success! now redirecting...
            <meta http-equiv="refresh" content="0;url=login.py?message={0}"/>'''.format(message))
    else:
        print('''Failed...now redirecting...
            <meta http-equiv="refresh" content="0;url=register.py?message={0}"/>'''.format(message))

def htmlMiddle():
    print('''
    <form action="try_register.py" method="post" id="register">
        username: <input type="text" name="username" required><br>
        password: <input type="password" name="password" required><br>
        password: <input type="password" name="retype password" required><br>
    </form>

    <button type="submit" form="register" value="Login">Login</button>''')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()
        formData = cgi.FieldStorage()
        username = formData.getvalue('username')
        password = formData.getvalue('password')
        password_check = formData.getvalue('password_check')
        if password != password_check:
            registerHTML(False, "password_not_match")
        else:
            success,message=db_util.create_user(username, password)
            registerHTML(success, message)
        htmlTail()
    except:
        cgi.print_exception()