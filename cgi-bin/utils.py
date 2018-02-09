# utils.py
import inspect
import sys
import os
from datetime import datetime

VERBOSE = True
LOGGING = True
LOGFILE = 'log.txt'
def add_edited(path):
    file_path = os.path.dirname(path)
    file_name = os.path.basename(path)
    new_path = os.path.join(file_path,'edited_'+file_name)
    return new_path

def rmv_edited(path):
    if "edited_" in path:
        file_path = os.path.dirname(path)
        file_name = '_'.join(os.path.basename(path).split('_')[1:])
        new_path = os.path.join(file_path,file_name)
        return new_path
    else:
        return path

def unlink_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
            done("done unlinking file because discard")
        else:
            log(file_path)
            log(os.getcwd())
    except Exception as error:
        err(error)

# TESTED!
def get_client_cookie():
    res=dict()
    if 'HTTP_COOKIE' in os.environ:
        cookies = os.environ['HTTP_COOKIE']
        # log("Real cookie: {0}".format(cookies))
        cookies = cookies.split('; ')
        for cookie in cookies:
            try:
                cookie_key, cookie_val = cookie.split('=')
                res[cookie_key] = cookie_val
            except:
                log("Cookie error:"+cookie)
                cookie_key = ""
                cookie_val = ""
    # log("Cookie evaluated: "+str(res))
    return res
# TESTED!
def err(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("Error@"+caller+': '+str(s))
        print("<br>")
        log("Error@"+caller+': '+str(s))

# TESTED!
def done(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("done@"+caller+": "+str(s))
        print("<br>")
        log("done@"+caller+": "+str(s))

def log(s):
    try:
        if LOGGING and VERBOSE: # incase someone call it directly
            f = open(LOGFILE,'a')
            time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            f.write(time+':\t'+str(s))
            f.write('\n')
            f.close()
    except:
        pass
        # probably broken pipe, etc
