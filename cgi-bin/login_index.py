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
        print("<br>Message: {0}<br>".format(message))

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
        print("<br>Message: {0}<br>".format(message))

def paging_html(total_page_number,current_page):
    total_page_number = int(total_page_number)
    current_page = int(current_page)
    if current_page >= total_page_number:
        disable_next = "disabled"
    else:
        disable_next = ""
    if current_page <= 1:
        disable_prev = "disabled"
    else:
        disable_prev = ""
    print('''
    <form action="login_index.py" method="POST" style="float: left;">
        <input type="submit" value="Previous page" name="page_option" {2}/>
        &nbsp;&nbsp;&nbsp;&nbsp;
        Page <input style="width: 20px;" type="text" name="page" value="{1}" placeholder="{1}"/> of {0}
        <input type="submit" value="OK" name="page_option" />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input type="submit" value="Next page" name="page_option" {3}/>
    </form>
    '''.format(total_page_number, current_page, disable_prev, disable_next))

def upload_image(username):
    print('''
    <h3>Upload Image</h2>
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

def instagram_feed(username, loggedin, page_number):
    try:
        page_number = int(page_number)
    except:
        print("Not a number")

    if loggedin:
        f = db_util.read_logged_image
    else:
        f = db_util.read_public_image

    success, res, total_page = f(username, page_number, 8)
    if page_number > total_page:
        page_number = total_page
        success, res, total_page = f(username, page_number, 8)
        print("page number requested greater than max page number")
    elif page_number < 1:
        page_number = 1
        success, res, total_page = f(username, page_number, 8)
        print("page number requested smaller than 1")

    if success:
        print "<p>"
        for i in range(len(res)):
            (path, timestamp) = res[i]
            resized_path = utils.add_resized(path)
            resized_path = os.path.join('..',resized_path)
            path = os.path.join('..',path)
            print('''
            <a style="text-decoration: none;" target="_blank" href="{1}" style="padding-bottom: 10px">
                <img style="padding-right: 10px;" src="{0}" alt="Something broke"/>
            </a>
                '''.format(resized_path, path))
            if i == 3:
                print "</p><p>"
        print "</p>"
        print('<p>')
        paging_html(total_page, page_number)
        print('</p>')
        for i in range(5):
            print("<br>")
        # print res
        # print('''all_instagram_feed fetch success''')
        # print('<br>')
    else:
        print('''all_instagram_feed fetch failed''')
        print(str(res))
        print('<br>')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        cookies = utils.get_client_cookie()
        # username = cookies.get('username',"ERROR")
        auth_cookie = cookies.get('cookie',"ERROR")
        get_username_success, username = db_util.get_username(auth_cookie)
        message = formData.getvalue('message', '')
        page_number = formData.getvalue('page', "1")
        page_option = formData.getvalue('page_option', '')
        utils.log(page_number)
        if not page_number.isdigit():
            print("Invalid page number entered, redirect to page 1")
            page_number = 1

        if page_option == "Next page":
            page_number = int(page_number)+1
        elif page_option == "Previous page":
            page_number = int(page_number)-1
        elif page_option == "OK":
            page_number = int(page_number)

        if get_username_success:
            auth_info(username,message)
            print "<hr>"
            upload_image(username)
            print "<hr>"
            instagram_feed(username,True,page_number)
        else:
            not_login_auth_info(message)
            print "<hr>"
            print "If you want to upload a photo, please login!"
            print "<hr>"
            instagram_feed(username,False,page_number)
        htmlTail()
    except:
        cgi.print_exception()
