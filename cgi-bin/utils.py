# utils.py
import inspect
VERBOSE = True
# TESTED!
def err(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("Error@"+caller+': '+str(s))
        print("<br>")

# TESTED!
def done(s):
    if VERBOSE:
        caller = inspect.stack(0)[1][3]
        print("done@"+caller+": "+str(s))
        print("<br>")
