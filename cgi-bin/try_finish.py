#!/usr/bin/python
# try_finish.cgi
import cgi
import db_util
import utils
import os

def htmlTop():
    print("Content-type:text/html")
    print("""
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Edit</title>
            </head>
        <body>""")

def discardHTMLMid(file_path):
    unlink_file(file_path)
    print("""You have chosen to discard, now redirecting...<meta http-equiv="refresh" content="0;url=login_index.py" />""")

def unlink_file(file_path):
    if os.path.isfile(file_path):
        os.unlink(file_path)
        utils.done("done unlinking file because discard")
    else:
        utils.log(file_path)
        utils.log(os.getcwd())

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        cookies = utils.get_client_cookie() # To ensure permission
        username = formData.getvalue('username')
        visibility = formData.getvalue('visibility')
        file_path = formData.getvalue('file_path')
        username = formData.getvalue('username')
        option = formData.getvalue('option')

        utils.log(file_path)
        if option == "Undo":
            utils.done(username+":Undo")
        elif option == "Discard":
            discardHTMLMid(file_path)
            utils.done(username+":Discard")
        elif option == "Finish":
            utils.done(username+":Finish")
        else:
            utils.err("option cannot be recognized {0}".format(option))

        htmlTail()
    except:
        cgi.print_exception()
