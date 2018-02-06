#!/usr/bin/python
# register.cgi
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
    <form action="try_register.py" method="post" id="register">
        username: <input type="text" name="username" required><br>
        password: <input type="password" name="password" required><br>
        retype password: <input type="password" name="password_check" required><br>
    </form>
    <button type="submit" form="register" value="Register">Register</button>''')
    if message != '':
        print ("<br>"+message)

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        message = formData.getvalue('message', "")
        if message == "password_not_match":
            htmlMid("Password does not match, please type again.")
        elif message == "user_exists":
            htmlMid("User exists, please change a username.")
        else:
            htmlMid(message)
        htmlTail()
    except:
        cgi.print_exception()
