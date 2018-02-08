#!/usr/bin/python
# upload_image.cgi
import db_util
import utils
import os
import cgi
import uuid
import subprocess
UPLOAD_PATH = "./upload"

def htmlTop():
    print("""Content-type:text/html\n\n
             <!DOCTYPE html>
             <html lang='en'>
                 <head>
                     <meta charset='utf-8'/>
                     <title>Upload image</title>
                 </head>
                 <body>""")

def loginMid(username):
    print('''Logging in with cookie! now redirecting... <meta http-equiv="refresh" content="0;url=login_index.py?username={0}" />
    '''.format(username))

def htmlMid():
    print('''<form method="post" action="login.py">
        <input type="submit" value="Login" method="post"/></form>
        <br>
        <form method="post" action="register.py">
        <input type="submit" value="Register" method="post"/></form>
    ''')

def htmlTail():
    print("""</body>
            </html>""")

def successHtmlMid(message=''):
    print("""<h1>Successfully uploaded image, you can edit it now</h1>
        """)
    if message!='':
        print(message)

def unsuccessHtmlMid(message=''):
    print("""<h1>Upload image failed, please try again</h1>
        """)
    if message!='':
        print(message)

def save_image(image_from_form):
    try:
        if image.file:
            # initialize
            full_filename = os.path.basename(image_from_form.filename)
            # save the image
            filename = full_filename.split('.')[0]
            file_extension = full_filename.split('.')[1]
            filename = filename+'_'+uuid.uuid4().hex[8:] # prevent collides
            full_filename = filename+'.'+file_extension
            path = os.path.join(UPLOAD_PATH, full_filename)
            with open(path, 'wb') as f:
                # NOTE: resize image when necessary here
                f.write(image_from_form.file.read())
            # identify if the image is valid
            # Identify output format: ['./upload/yr3sem2cusis_b7bc47388f6134a559a69a03.png', 'PNG', '1852x1092', '1852x1092+0+0', '8-bit', 'sRGB', '360167B', '0.000u', '0:00.000\n']
            proc = subprocess.Popen(["identify", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if out:
                image_iden = out.split(' ')
                image_ext = image_iden[1]
                image_size = image_iden[2]
                shown_ext = full_filename.split('.')[-1]
                if image_ext.upper() != shown_ext.upper():
                    utils.err("{0}: image extension does not match: shown {2}, but actually {1}".format(full_filename, image_ext, shown_ext))
                    return (False, "image extension does not match")
            elif err:
                return (False, "target is not a image")
                utils.err(err)
            return (True,path)
        else:
            utils.log("{0}: Tries to upload an image but failed!".format(username))
            utils.log("filename:"+str(image.filename))
            utils.log("headers:"+str(image.headers))
            utils.log("value:"+str(image.value))
            utils.log("basename:"+str(os.path.basename(image.value)))
            utils.log("type:"+str(image.type))
            utils.log("disposition:"+str(image.disposition))
            utils.log("list:"+str(image.list))
            return (False, "cannot open image")
    except Exception as error:
        utils.err(error)
        return (False,str(error))

if __name__ == '__main__':
    try:
        htmlTop()
        cookies = utils.get_client_cookie()
        formData = cgi.FieldStorage()
        username = formData.getvalue('username',"ERROR")
        image = formData['image']
        success, message = save_image(image)
        if success:
            successHtmlMid(message)
        else:
            unsuccessHtmlMid(message)
        htmlTail()
    except:
        cgi.print_exception()
