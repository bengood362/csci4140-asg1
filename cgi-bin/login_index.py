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

def not_login_auth_info(message=''):
    print('''<h2>Hello!</h2>
    <form action="login.py" method="post" id="logout">
        <input type="submit" value="Login" method="post"/>
    </form>
    <form action="register.py" method="post" id="change">
        <input type="submit" value="Register" method="post"/>
    </form>
    ''')
    if message != '':
        print("<br>{0}<br>".format(message))

def auth_info(username, message=''):
    print('''<h2>Hello {0}!</h2>
    <form action="try_logout.py" method="post" id="logout">
        <input type="hidden" name="username" value="{0}" />
        <input type="submit" value="Logout" method="post"/>
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

def all_instagram_feed(username, page_number):
    success, res = db_util.read_logged_image(username, page_number, 8)
    if success:
        for (path, timestamp) in res:
            resized_path = utils.add_resized(path)
            resized_path = os.path.join('..',resized_path)
            path = os.path.join('..',path)
            print('''
            <p><a href="{1}">
                <img src="{0}" alt="Something broke"/>
            </a></p>
                '''.format(resized_path, path))
        # print res
        # print('''all_instagram_feed fetch success''')
        # print('<br>')
    else:
        print('''all_instagram_feed fetch failed''')
        print(str(res))
        print('<br>')

def public_instagram_feed(page_number):
    success, res = db_util.read_public_image(page_number, 8)
    if success:
        for (path, timestamp) in res:
            resized_path = utils.add_resized(path)
            resized_path = os.path.join('..',resized_path)
            path = os.path.join('..',path)
            print('''
            <p><a href="{1}">
                <img src="{0}" alt="Something broke"/>
            </a></p>
                '''.format(resized_path, path))
        # print res
        # print('''public_instagram_feed fetch success''')
        # print('<br>')
    else:
        print('''public instagram feed fetch failed''')
        print(str(res))
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
        page_number = formData.getvalue('page', '1')

        htmlTop()
        if get_username_success:
            auth_info(username,message)
            print "<hr>"
            upload_image(username)
            print "<hr>"
            all_instagram_feed(username,page_number)
        else:
            not_login_auth_info(message)
            print "<hr>"
            print "If you want to upload a photo, please login!"
            print "<hr>"
            public_instagram_feed(page_number)
        htmlTail()
    except:
        cgi.print_exception()
