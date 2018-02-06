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
        htmlMid()
        htmlTail()
    except:
        cgi.print_exception()
