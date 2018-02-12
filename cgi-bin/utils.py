# utils.py
import inspect
import sys
import os
import subprocess
from datetime import datetime

VERBOSE = False
LOGGING = False
LOGFILE = 'log.txt'

def resize_to_200(file_path):
    new_path = add_resized(file_path)
    cmds = ["convert",file_path,'-resize','200x200',new_path]
    p=subprocess.Popen(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, error = p.communicate()
    if error:
        err(error)
        return (False, str(error))
    return (True, new_path)

def get_dim(path):
    try:
        cmds=['identify','-format','%wx%hx',path]
        p = subprocess.Popen(cmds, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, error = p.communicate()
        size = out.split('x')
        width = size[0]
        height = size[1]
        return (True, (int(width), int(height)))
    except Exception as error:
        err(error)
        return (False, error)

def add_resized(path):
    file_path = os.path.dirname(path)
    file_name = os.path.basename(path)
    new_path = os.path.join(file_path,'resized_'+file_name)
    return new_path

def add_edited(path):
    file_path = os.path.dirname(path)
    file_name = os.path.basename(path)
    new_path = os.path.join(file_path,'edited_'+file_name)
    return new_path

def rmv_resized(path):
    if "resized" in path:
        file_path = os.path.dirname(path)
        file_name = '_'.join(os.path.basename(path).split('_')[1:])
        new_path = os.path.join(file_path,file_name)
        return new_path
    else:
        return path

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
            done("done unlinking file because discard/ undo")
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
