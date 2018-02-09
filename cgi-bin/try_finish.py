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

def discardHTMLMid():
    print("""You have chosen to discard, now redirecting...<meta http-equiv="refresh" content="0;url=login_index.py" />""")

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
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        if option == "Discard":
            try:
                utils.unlink_file(file_path)
                removed_path = utils.rmv_edited(file_path)
                if removed_path != file_path:
                    utils.unlink_file(removed_path)
                discardHTMLMid()
            except:
                # In case it does not have any edit
                pass
            utils.done(username+":Discard")
        elif option == "Finish": # Should become edited_XXXXXX.EXT too, because I am lazy
            utils.done(username+":Finish")
        else:
            utils.err("option cannot be recognized {0}".format(option))

        htmlTail()
    except:
        cgi.print_exception()
