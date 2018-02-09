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
                <title>Web Instagram</title>
            </head>
        <body><h1>Web instagram</h1>""")

def auth_info(username, message=''):
    print('''<h2>Hello {0}!</h2>
    <form action="try_logout.py" method="post" id="logout">
        <input type="hidden" name="username" value="{0}" />
        <input type="submit" value="logout" method="post"/>
    </form>
    <form action="change_password.py" method="post" id="change">
        <input type="hidden" name="username" value="{0}" />
        <input type="submit" value="Change password" method="post"/>
    </form>
    '''.format(cgi.escape(username)))
    if message != '':
        print("<br>{0}<br>".format(message))

def upload_image(username):
    print('''
    <form action="upload_image.py" method="POST" enctype="multipart/form-data" id="img_upload">
        <input type="hidden" name="username" value="{0}" />
        <input type="file" name="image" id="image" accept="image/jpeg,image/jpg,image/gif,image/png" required/>
        <br>
        visibility: <select name="visibility">
          <option value="public">public</option>
          <option value="private">private</option>
        </select>
        <br><br>
        <input type="submit" name="submit" value="Upload" method="post" form="img_upload"/>
    </form>
    '''.format(username))

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
        # username = cookies.get('username',"ERROR")
        auth_cookie = cookies.get('cookie',"ERROR")
        get_username_success, username = db_util.get_username(auth_cookie)
        message = formData.getvalue('message', '')

        htmlTop()

        auth_info(username,message)
        print "<hr>"
        upload_image(username)
        print "<hr>"
        instagram_feed(5)

        htmlTail()
    except:
        cgi.print_exception()
