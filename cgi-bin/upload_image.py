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
        disabled_undo = "disabled"
        disabled_fin = ""
    else:
        disabled_undo = ""
        disabled_fin = "disabled"
    print("""<h1>Edit photo</h1>
    <img src="{0}" width="600" alt='Something is broken'/>
    <form method="post" action="upload_image.py" id="change_filter"/>
        <input type="hidden" value={2} name="visibility"/>
        <input type="hidden" value={1} name="username"/>
        <input type="hidden" value={5} name="file_path"/>
        <input type="hidden" value={3} name="filter"/>
        <input type="submit" value="Border" name="filter_chosen" {6}/>
        <input type="submit" value="Lomo" name="filter_chosen" {6}/>
        <input type="submit" value="Lens_Flare" name="filter_chosen" {6}/>
        <input type="submit" value="Black_White" name="filter_chosen" {6}/>
        <input type="submit" value="Blur" name="filter_chosen" {6}/>
    </form>
    <hr>
    <form method="post" action="upload_image.py" id="undo" style="display: inline;">
        <input type="hidden" value={2} name="visibility"/>
        <input type="hidden" value={1} name="username"/>
        <input type="hidden" value={5} name="file_path"/>
        <input type="hidden" value=None name="filter_chosen"/>
        <input type="submit" value="Undo" name="option" {4}/>
    </form>
    <form method="post" action="try_finish.py" id="finish">
        <input type="hidden" value={2} name="visibility"/>
        <input type="hidden" value={1} name="username"/>
        <input type="hidden" value={5} name="file_path"/>
        <input type="hidden" value={3} name="filter_chosen"/>
        <input type="submit" value="Discard" name="option" /><br>
        <input type="submit" value="Finish" name="option" />
    </form>
        """.format(cgi.escape(new_file_path), username, visibility, filter_chosen, disabled_undo, cgi.escape(file_path), disabled_fin))


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
            # save the image at UPLOAD_PATH (./upload)
            filename = '.'.join(full_filename.split('.')[:-1])
            file_extension = full_filename.split('.')[-1]
            filename = filename+'_'+uuid.uuid4().hex[8:] # prevent collides
            full_filename = filename+'.'+file_extension
            path = os.path.join(UPLOAD_PATH, full_filename)
            with open(path, 'wb+') as f:
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
        return (True, file_path)
    elif filter_chosen == "Border":
        new_path = utils.add_edited(file_path)
        cmds = ["convert",file_path,"-bordercolor","black","-border","7", new_path]
        utils.log(user+": "+" ".join(cmds))
        p=subprocess.Popen(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            utils.done(out)
            return (True, new_path)
        if err:
            utils.err(err)
            return (False, str(err))
        return (True, new_path)
    elif filter_chosen == "Lomo":
        new_path = utils.add_edited(file_path)
        cmds = ["convert", file_path, "-channel", 'R', '-level', '33%', '-channel', 'g', '-level', '33%', new_path]
        utils.log(user+": "+" ".join(cmds))
        p=subprocess.Popen(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            utils.done(out)
            return (True, new_path)
        if err:
            utils.err(err)
            return (False, str(err))
        return (True, new_path)
    elif filter_chosen == "Lens_Flare":
        success, message = utils.get_dim(file_path)
        if success:
            size = message
            (width, height) = size
            new_path = utils.add_edited(file_path)
            cmds1=['convert','./lensflare.png','-resize',str(width)+'x', './tmp.png']
            cmds2=['composite','-compose','screen','-gravity','northwest','./tmp.png',file_path,new_path]
            p1=subprocess.Popen(cmds1, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p1.communicate()
            if err:
                utils.err(err)
                return (False, str(err))
            p2=subprocess.Popen(cmds2, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p2.communicate()
            if out:
                utils.done(out)
                return (True, new_path)
            if err:
                return (False, str(err))
            return (True, new_path)
        else:
            return (False, message)
        pass
    elif filter_chosen == "Black_White":
        pass
    elif filter_chosen == "Blur":
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        new_path = utils.add_edited(file_path)
        cmds = ["convert", file_path, '-blur', '0.5x2', new_path]
        utils.log(user+": "+" ".join(cmds))
        p=subprocess.Popen(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            utils.done(out)
            return (True, new_path)
        if err:
            utils.err(err)
            return (False, str(err))
        return (True, new_path)
    else:
        utils.err("The filter cannot be recognized: {0}".format(filter_chosen))
        return (False, "The filter cannot be recognized: {0}".format(filter_chosen))

if __name__ == '__main__':
    try:
        htmlTop()
        cookies = utils.get_client_cookie()
        formData = cgi.FieldStorage()
        username = formData.getvalue("username","ERROR")
        visibility = formData.getvalue("visibility", "public")
        filter_chosen = formData.getvalue("filter_chosen", "None")
        file_path = formData.getvalue("file_path")
        option = formData.getvalue("option")
        if option and option == "Undo":
            file_path_after_undo = utils.rmv_edited(file_path)
            utils.unlink_file(file_path)
            startEditHtmlMid(file_path_after_undo, username, visibility, filter_chosen)
            pass
        else:
            if file_path: # comes from edit
                success, message = edit_image(file_path, filter_chosen, username)
            else: # comes from main
                image = formData['image']
                success, message = save_image(image, username)

            if success:
                file_path=message
                utils.done(username+":image saved and validated")
                startEditHtmlMid(file_path, username, visibility, filter_chosen)
            else:
                unsuccessHtmlMid(message)
            htmlTail()
    except:
        cgi.print_exception()
