import uuid

from redis import Redis

__db = Redis()
__db_table_sessions = "cholewp1:webapp:v4:session"


def create_new_session(username):
    sid = str(uuid.uuid4())
    __db.hset(__db_table_sessions, sid, username)
    return sid


def check_session_valid(username, sid):
    db_user = __db.hget(__db_table_sessions, sid).decode('utf-8')
    if db_user is None:
        return False
    if db_user == username:
        return True
    return False


def delete_session(sid):
    __db.hdel(__db_table_sessions, sid)
