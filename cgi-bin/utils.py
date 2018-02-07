# utils.py
import inspect
import sys
from datetime import datetime
VERBOSE = True
LOGFILE = 'log.txt'
# TESTED!
def err(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("Error@"+caller+': '+str(s))
        print("<br>")
        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        log(time+":\tError@"+caller+': '+str(s))

# TESTED!
def done(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("done@"+caller+": "+str(s))
        print("<br>")
        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        log(time+":\tdone@"+caller+": "+str(s))

def log(s):
    with open(LOGFILE,'a+') as f:
        f.write(str(s))
        f.write('\n')
