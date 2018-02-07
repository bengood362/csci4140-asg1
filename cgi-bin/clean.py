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

def cleanHTML(success, message):
    if success:
        print('''Clean success! now redirecting...<meta http-equiv="refresh" content="0;url=../index.html" />''')
    else:
        print('''Clean failed! now redirecting... <meta http-equiv="refresh" content="0;url=../index.html" />
            ''')

def htmlTail():
    print('''</body>
        </html>''')

if __name__ == '__main__':
    try:
        htmlTop()

        formData = cgi.FieldStorage()
        success,message = db_util.clean_table(db_util.USER_TABLE)
        cleanHTML(success, message)

        htmlTail()
    except:
        cgi.print_exception()
