#!/usr/bin/python
# clean.py
import time
import cgi
import db_util

def htmlTop():
    print("""Content-type:text/html\n\n
        <!DOCTYPE html>
        <html lang='en'>
            <head>
                <meta charset='utf-8'/>
                <title>Try logging in...</title>
            </head>
        <body>""")

def cleanHTML(success, message=''):
    if success:
        print('''Clean success! now redirecting...<meta http-equiv="refresh" content="0;url=../index.html?message={0}" />'''.format(cgi.escape(message)))
    else:
        print('''Clean failed! now redirecting... <meta http-equiv="refresh" content="0;url=../index.html={0}" />
            '''.format(cgi.escape(message)))
    if message != '':
        print message

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        success, message = db_util.remove_table(db_util.USER_TABLE)
        success2, message2 = db_util.remove_table(db_util.IMAGE_TABLE)
        cleanHTML(success and success2, message+', '+message2)

        htmlTail()
    except:
        cgi.print_exception()
