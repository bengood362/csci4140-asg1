#!/usr/bin/python
# upload_image.cgi
# NOTE: EDIT TAKE PLACES HERE

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

def startEditHtmlMid(file_path, username, visibility, filter_chosen="None"):
    new_file_path = os.path.join("..",file_path) #upload not in cgi bin
    if filter_chosen == "None":
        disabled = "disabled"
    else:
        disabled = ""
    print("""<h1>Edit photo</h1>
    <img src="{0}" width="600" alt='Something is broken'/>
    <form method="post" action="upload_image.py" id="change_filter"/>
        <input type="hidden" value={2} name="visibility"/>
        <input type="hidden" value={1} name="username"/>
        <input type="hidden" value={0} name="file_path"/>
        <input type="hidden" value={3} name="filter"/>
        <input type="submit" value="Border" name="filter" />
        <input type="submit" value="Lomo" name="filter" />
        <input type="submit" value="Lens_Flare" name="filter" />
        <input type="submit" value="Black_White" name="filter" />
        <input type="submit" value="Blur" name="filter" />
    </form>
    <hr>
    <form method="post" action="try_finish.py" id="finish">
        <input type="hidden" value={2} name="visibility"/>
        <input type="hidden" value={1} name="username"/>
        <input type="hidden" value={5} name="file_path"/>
        <input type="hidden" value={3} name="filter"/>
        <input type="submit" value="Undo" name="option" {4}/>
        <input type="submit" value="Discard" name="option" />
        <input type="submit" value="Finish" name="option" />
    </form>
        """.format(cgi.escape(new_file_path), username, visibility, filter_chosen, disabled, cgi.escape(file_path)))


def unsuccessHtmlMid(message=''):
    print("""<h1>Upload image failed, please try again</h1>
        """)
    if message!='':
        print(message)
    print '''<form action="login_index.py">
                <input type="submit" value="back"/>
            </form>'''

def ext_equal(ext1, ext2):
    res = ext1.lower() == ext2.lower()
    if ext1.lower() == 'jpeg' and ext2.lower() == 'jpg':
        res = True
    if ext2.lower() == 'jpeg' and ext1.lower() == 'jpg':
        res = True
    return res

def save_image(image_from_form, username):
    try:
        if image.file:
            # initialize
            full_filename = os.path.basename(image_from_form.filename)
            # save the image
            filename = '.'.join(full_filename.split('.')[:-1])
            file_extension = full_filename.split('.')[-1]
            filename = filename+'_'+uuid.uuid4().hex[8:] # prevent collides
            full_filename = filename+'.'+file_extension
            path = os.path.join(UPLOAD_PATH, full_filename)
            with open(path, 'wb') as f:
                f.write(image_from_form.file.read())
            # identify if the image is valid
            # Identify output format: ['./upload/yr3sem2cusis_b7bc47388f6134a559a69a03.png', 'PNG', '1852x1092', '1852x1092+0+0', '8-bit', 'sRGB', '360167B', '0.000u', '0:00.000\n']
            proc = subprocess.Popen(["identify", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if out:
                image_iden = out.split(' ')
                image_ext = image_iden[-8] #There might be some filename with space
                image_size = image_iden[-7]
                shown_ext = file_extension
                if not ext_equal(shown_ext, image_ext):
                    utils.err("{0} {3}: image extension does not match: shown {2}, but actually {1}".format(username, image_ext, shown_ext, full_filename))
                    return (False, "image extension does not match")
            elif err:
                return (False, "target is not a image")
                utils.err(username+':'+err)
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
            utils.err(username+err)
            return (False, "cannot open image")
    except Exception as error:
        utils.err(username+':'+str(error))
        return (False,str(error))

def edit_image(file_path, filter_chosen, user):
    if filter_chosen == "None":
        pass
    elif filter_chosen == "Border":
        pass
    elif filter_chosen == "Lomo":
        pass
    elif filter_chosen == "Lens_Flare":
        pass
    elif filter_chosen == "Black_White":
        pass
    elif filter_chosen == "Blur":
        pass
    else:
        utils.err("The filter cannot be recognized: {0}".format(filter_chosen))

if __name__ == '__main__':
    try:
        htmlTop()
        cookies = utils.get_client_cookie()
        formData = cgi.FieldStorage()
        username = formData.getvalue("username","ERROR")
        visibility = formData.getvalue("visibility", "public")
        filter_chosen = formData.getvalue("filter", "None")
        file_path = formData.getvalue("file_path")
        if file_path: # comes from edit
            edit_image(file_path, filter_chosen, username)
            pass
        else: # comes from main
            image = formData['image']
            success, message = save_image(image, username)

        if success:
            utils.done(username+":image saved and validated")
            startEditHtmlMid(message, username, visibility)
        else:
            unsuccessHtmlMid(message)
        htmlTail()
    except:
        cgi.print_exception()
