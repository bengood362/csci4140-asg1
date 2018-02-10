#!/usr/bin/python
# try_change_password.cgi
import cgi
import db_util
import utils
def htmlTop():
    print("Content-type:text/html")
    print("""
        <!DOCTYPE html>
        <html lang='en'>
             <head>
                 <meta charset='utf-8'/>
                 <title>Change password</title>
             </head>
         <body>""")

def redirectMid(success, message, username):
    if success:
        print('''Success! now redirecting...
            <meta http-equiv="refresh" content="0;url=login_index.py?message={0}"/>'''.format(cgi.escape(message)))
    else:
        print('''Failed...now redirecting...
            <meta http-equiv="refresh" content="0;url=change_password.py?message={0}"/>'''.format(cgi.escape(message)))


def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        cookies = utils.get_client_cookie()
        auth_cookie = cookies.get('cookie','')
        success, message = db_util.get_username(auth_cookie)
        if success:
            username = message
        else:
            username = "ERROR"
        password_o = formData.getvalue('password_o','')
        password_n = formData.getvalue('password_n','')
        password_n2 = formData.getvalue('password_n2','')

        if password_n != password_n2:
            redirectMid(False, "new password does not match", username)
        else:
            success, message = db_util.update_user(username, password_o, password_n)
            redirectMid(success, message, username)
        htmlTail()
    except:
        cgi.print_exception()
