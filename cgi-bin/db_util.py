# db_util.py
from datetime import datetime
import sqlite3
import os
import inspect
import uuid #uuid4() --> cookie
from utils import err, done,log
try:
    # log(os.environ['GATEWAY_INTERFACE'])
    if 'cgi' in os.environ['GATEWAY_INTERFACE'].lower():
        DATABASE = 'csci4140.db'
    else:
        DATABASE = "csci4140.db"
except:
    DATABASE = "csci4140.db"
# Should not modify USER_TABLE and IMAGE_TABLE!!!!!!!
USER_TABLE = "user"
IMAGE_TABLE = "image_link"
"""
@ DatabaseInstance has these object:
- conn | connection
- curs | cursor

csci4140.db
@@@ admin @@@
| username: TEXT
| password: TEXT
@@@ user @@@
| username: TEXT
| password: TEXT
| cookie: TEXT
@@@ image_link @@@
| owner: TEXT
| private: INTEGER (1/ 0)
| image_url: TEXT
| timestamp: DATETIME
"""

# Singleton
class DatabaseInstance(object):
    @staticmethod
    def init_db(database):
        try:
            conn = sqlite3.connect(database)
            curs = conn.cursor()
            curs.execute('''CREATE TABLE IF NOT EXISTS user (
                username TEXT PRIMARY KEY,
                password TEXT,
                cookie TEXT
            )''')
            curs.execute('''CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                password TEXT
            )''')
            curs.execute('''CREATE TABLE IF NOT EXISTS image_link (
                owner TEXT,
                private INTEGER,
                image_url TEXT,
                Timestamp TEXT
            )''')
            conn.commit()
            return conn, curs
        except Exception as error:
            err(str(error))
            return None, None

DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db(DATABASE)

# DEBUG
def debug():
    clean_table(USER_TABLE)
    remove_table(USER_TABLE)
    clean_table(PUBLIC_IMAGE_TABLE)
    remove_table(PUBLIC_IMAGE_TABLE)
    clean_table(PRIVATE_IMAGE_TABLE)
    remove_table(PRIVATE_IMAGE_TABLE)
    reset_conn()
    DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db(DATABASE)
    create_user("bengood362","123456")
    create_user("benben123","123456")
    create_user("benben123","456789")
    create_user("ben123","456789")
    print list_table(USER_TABLE)
    update_user("bengood362","234567","987654")
    print list_table(USER_TABLE)
    update_user("bengood362","123456","987654")
    print list_table(USER_TABLE)
    print login_user("bengood362", "987654")
    print table_len(USER_TABLE)
    reset_conn()
    print login_user("bengood362", "987654")
    print list_table(USER_TABLE)

### Image method
# Timestamp will be automatically generated by SQLite3
def create_image(username, visibility, image_link):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        if visibility == "public":
            private = 0
        else:
            private = 1
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # Image name statistically won't collide because there is uuid.uuid4().hex[8:] appended
        curs.execute("INSERT INTO image_link VALUES('{0}',{1},'{2}','{3}')".format(username, private, image_link, timestamp))
        conn.commit()
        done(username+":create image success")
        return (True, "create_image_success")
    except Exception as error:
        err(error)
        return (False,str(error))

def read_public_image(username, page_number, limit=8):
    try:
        page_number = int(page_number)
        limit = int(limit)
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        res = curs.execute("SELECT image_url, Timestamp FROM image_link WHERE private=0 ORDER BY Timestamp DESC").fetchall()
        index_from = min(len(res),(page_number-1)*limit)
        index_to = min(len(res),(page_number)*limit)
        photo_links = res[index_from:index_to]
        done("successfully fetched public images")
        total_page = max(1, ((len(res)-1)//8)+1)
        return (True, photo_links, total_page)
    except Exception as error:
        err(error)
        return (False,str(error), 0)

def read_logged_image(username, page_number, limit=8):
    try:
        page_number = int(page_number)
        limit = int(limit)
        username = str(username)
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        res = curs.execute("SELECT image_url, Timestamp FROM image_link WHERE ((owner='{0}' and private=1) or (private=0)) ORDER BY Timestamp DESC".format(username)).fetchall()
        index_from = min(len(res),(page_number-1)*limit)
        index_to = min(len(res),(page_number)*limit)
        photo_links = res[index_from:index_to]
        done("successfully fetched public images")
        total_page = max(1, ((len(res)-1)//8)+1)
        return (True, photo_links, total_page)
    except Exception as error:
        err(error)
        return (False,str(error), 0)

### User method
# TESTED! check if user exists -> create
def admin_exist():
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        length = len(curs.execute("SELECT rowid FROM admin").fetchall())
        if length == 0:
            return False
        else:
            return True
    except Exception as error:
        err(error)
        return True

def create_admin(password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        curs.execute("INSERT INTO admin VALUES('{0}','{1}');".format("Admin", password))
        conn.commit()
        done("create admin success")
        return (True, "change admin password success")
    except Exception as error:
        err(str(error))
        return (False, str(error))

def login_admin(password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        rowid = curs.execute("SELECT rowid FROM admin WHERE username='{0}' and password='{1}'".format("Admin", password)).fetchall()
        if rowid != 0:
            return (True,"login success")
        else:
            return (False,"wrong password")
    except Exception as error:
        err(error)
        return (False, str(err))

def create_user(username, password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        user_not_exist = not entry_exist(USER_TABLE, "username", username)
        if user_not_exist:
            curs.execute("INSERT INTO user VALUES('{0}','{1}', NULL);".format(username, password))
            conn.commit()
            done(username+":create user success")
            return (True, "register_success")
        else:
            err(username+":user exists")
            return (False, "user_exists")
    except Exception as error:
        err(username+str(error))
        return (False, str(error))

def get_username(cookie):
    try:
        curs = DatabaseInstance.curs
        usernames = curs.execute("SELECT username FROM user WHERE cookie='{0}'".format(cookie)).fetchall()
        if len(usernames) != 0:
            username = usernames[0][0]
            if username == None:
                err("Cannot find username with such user cookie, please login")
                return (False,'Cannot find username with such user cookie, please login')
            else:
                done("Username is retrieved by this cookie {0}".format(cookie))
                return (True,username)
        else:
            err("Cannot find any user with such cookie")
            return (False,'Cannot find any user with such cookie')
    except Exception as error:
        err(error)
        return (False,error)

#For find matching cookie with username
def get_cookie(username):
    try:
        curs = DatabaseInstance.curs
        cookies = curs.execute("SELECT cookie FROM user WHERE username='{0}'".format(username)).fetchall()
        if len(cookies) != 0:
            cookies = cookies[0][0]
            if cookies == None:
                err("Cannot find cookie with such user name, please login")
                return (False,"Cannot find cookie with such user name, please login")
            else:
                done("Cookie retrieved for {0}".format(username))
                return (True,cookies)
        else:
            return (False,"Cannot find any user with such user name")
    except Exception as error:
        err(error)
        return (False,error)

#NOTE: duplicate of get_username(cookie), but I don't have the heart to delete it...
def resume_session(cookie):
    try:
        curs = DatabaseInstance.curs
        users = curs.execute("SELECT username FROM user WHERE cookie='{0}'".format(cookie)).fetchall()
        if len(users) == 0:
            err("Cookie invalid, please try to clean cookie from browser")
            return False
        return True
    except Exception as error:
        err(error)
        return False

# clean cookies
def logout(username):
    try:
        curs = DatabaseInstance.curs
        conn = DatabaseInstance.conn
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        curs.execute("UPDATE user SET cookie=NULL WHERE username='{0}';".format(username))
        conn.commit()
        done(username+":logout")
        return (True,'')
    except Exception as error:
        err(username+str(error))
        return (False, str(error))

# TESTED!
def login_user(username, password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        success = len(curs.execute("SELECT * from user WHERE username='{0}' AND password='{1}';".format(username, password)).fetchall()) >= 1
        if success:
            cookie=uuid.uuid4().hex
            p=curs.execute("UPDATE user SET cookie='{0}' WHERE username='{1}';".format(cookie, username))
            conn.commit()
            done(username+":login success, {0}".format(cookie))
            return (True,'login success')
        else:
            err(username+":wrong password")
            return (False,"wrong_password")
    except Exception as error:
        err(username+str(error))
        return (False,str(error))

# TESTED! check if old_pass correct --> update
def update_user(username, old_pass, password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        res = curs.execute("SELECT password FROM user WHERE username='{0}'".format(username)).fetchone()
        if res == None:
            err(username+":password cannot be fetched for this user")
            return (False,username+":pasword cannot be fetched for this user")
        saved_pass = res[0]
        if saved_pass != old_pass:
            err(username+":old password is incorrect")
            return (False,"old password does not match")
        else:
            curs.execute("UPDATE user SET password='{0}' WHERE username='{1}';".format(password, username))
            conn.commit()
            done(username+":password changed")
            return (True,'password has changed')
    except Exception as error:
        err(username+str(error))
        return (False,str(error))

# common method
# TESTED!
def entry_exist(tablename, column_key, column_val):
    try:
        curs = DatabaseInstance.curs
        stmt = "SELECT EXISTS(SELECT * FROM {0} WHERE {1}='{2}')".format(tablename, column_key, column_val)
        res = curs.execute(stmt).fetchone()[0]
        # done("entry_exist checked with {0},{1},{2},output {3}".format(tablename, column_key, column_val, res!=0))
        return res != 0
    except Exception as error:
        err(error)
        return True

# TESTED!
def list_table(tablename):
    try:
        curs = DatabaseInstance.curs
        return curs.execute("SELECT * FROM {0}".format(tablename)).fetchall()
    except Exception as error:
        err(error)
        return False

# TESTED!
def table_len(tablename):
    try:
        curs = DatabaseInstance.curs
        return len(curs.execute("SELECT * from {0};".format(tablename)).fetchall())
        return True
    except Exception as error:
        err(error)
        return False

# TESTED!
def clean_table(tablename):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        curs.execute("DELETE FROM {0};".format(tablename))
        conn.commit()
        done("table cleaned for {0}".format(tablename))
        return (True,'clean successfully')
    except Exception as error:
        err(error)
        return (False,str(error))

# TESTED!
def remove_table(tablename):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        curs.execute("DROP TABLE {0};".format(tablename))
        conn.commit()
        done("table removed for {0}".format(tablename))
        return (True,"Success")
    except Exception as error:
        err(error)
        return (False,str(error))

# TESTED!
def reset_conn():
    try:
        close_conn()
        DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db(DATABASE)
        return True
    except Exception as error:
        err(error)
        return False

# TESTED!
def close_conn():
    try:
        conn = DatabaseInstance.conn
        conn.close()
        DatabaseInstance.conn = None
        DatabaseInstance.curs = None
        return True
    except Exception as error:
        err(error)
        return False

if __name__ == "__main__":
    pass
