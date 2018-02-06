# db_util.py
from datetime import datetime
import sqlite3
import os
import inspect
from utils import err, done

DATABASE = 'csci4140.db'
USER_TABLE = "user"
IMAGE_TABLE = "image_link"
"""
@ DatabaseInstance has these object:
- conn | connection
- curs | cursor

csci4140.db
@@@ user @@@
| username: TEXT
| password: TEXT
| cookie: TEXT
| cookie_expire: DATETIME
@@@ image_link @@@
| owner: TEXT
| image_url: TEXT
| timestamp: TEXT
"""
# NOTE: cookie should be expire whenever logout? not by any time

# Singleton
class DatabaseInstance(object):
    @staticmethod
    def init_db():
        try:
            conn = sqlite3.connect(DATABASE)
            curs = conn.cursor()
            curs.execute('''CREATE TABLE IF NOT EXISTS user (
                username TEXT PRIMARY KEY,
                password TEXT,
                cookie TEXT,
                cookie_expire DATETIME
            )''')
            curs.execute('''CREATE TABLE IF NOT EXISTS image_link (
                owner TEXT,
                image_url TEXT,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            return conn, curs
        except Exception as error:
            err(username+str(error))
            return False

DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db()

# DEBUG
def debug():
    clean_table(USER_TABLE)
    remove_table(USER_TABLE)
    reset_conn()
    DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db()
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

### user method
# TESTED! check if user exists -> create
def create_user(username, password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        user_not_exist = not entry_exist(USER_TABLE, "username", username)
        if user_not_exist:
            curs.execute("INSERT INTO user VALUES('{0}','{1}', NULL, NULL);".format(username, password))
            conn.commit()
            done(username+"create user success")
            return (True, "register_success")
        else:
            err(username+"user exists")
            return (False, "user_exists")
    except Exception as error:
        err(username+str(error))
        return (False, str(error))

#NOTE: still thinking, not finished
def resume_session(cookie):
    try:
        curs = DatabaseInstance.curs
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        curs.execute("SELECT cookie")
        return True
    except Exception as error:
        err(error)
        return False

def logout(username):
    try:
        curs = DatabaseInstance.curs
        conn = DatabaseInstance.conn
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        curs.execute("UPDATE user SET cookie_expire='{0}' and cookie=NULL WHERE username='{1}'".format(now, username))
        conn.commit()
        done(username+":logout")
        return (True,'')
    except Exception as error:
        err(username+str(error))
        return (False, str(error))

# TESTED!
def login_user(username, password):
    try:
        curs = DatabaseInstance.curs
        success = len(curs.execute("SELECT * from user WHERE username='{0}' AND password='{1}';".format(username, password)).fetchall()) >= 1
        if success:
            done(username+":login success")
            return (True,'')
        else:
            err(username+"wrong password")
            return (False,"wrong_password")
    except Exception as error:
        err(username+str(error))
        return (False,str(error))

# TESTED! check if old_pass correct --> update
def update_user(username, old_pass, password):
    try:
        conn = DatabaseInstance.conn
        curs = DatabaseInstance.curs
        saved_pass = curs.execute("SELECT password FROM user WHERE username='{0}'".format(username)).fetchone()[0]
        if saved_pass != old_pass:
            err(username+":old password is incorrect")
            return (False,"old_not_match")
        else:
            curs.execute("UPDATE user SET password='{0}' WHERE username='{1}'".format(password, username))
            conn.commit()
            done(username+":password changed")
            return (True,'')
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
        return True
    except Exception as error:
        err(error)
        return False

# TESTED!
def remove_table(tablename):
    try:
        curs = DatabaseInstance.curs
        curs.execute("DROP TABLE {0};".format(tablename))
        return True
    except Exception as error:
        err(error)
        return False

# TESTED!
def reset_conn():
    try:
        close_conn()
        DatabaseInstance.conn, DatabaseInstance.curs = DatabaseInstance.init_db()
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
