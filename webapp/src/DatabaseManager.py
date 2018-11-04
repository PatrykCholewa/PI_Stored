from src.UserClass import UserClass
from redis import Redis


__db = Redis()
__dbrecord_prefix = "cholewp1:webapp:v4"


def get_user_by_username(username):
    db_record = __db.hget(__dbrecord_prefix, username)
    if db_record is None:
        return None
    user = UserClass(db_record.decode('utf-8'))
    if user.username == username:
        return user

    return None


def _add_user_to_db(user):
    db_user = get_user_by_username(user.username)
    if db_user is not None:
        return False
    else:
        dbrecord = user.to_dbrecord()
        __db.hset(__dbrecord_prefix, user.username, dbrecord)
        return True


def add_new_user(username, password):
    user = UserClass.create_user(username, password)
    if _add_user_to_db(user):
        return user
    else:
        return None


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user is None:
        return False

    if user.check_password(password):
        return True
    else:
        return False
