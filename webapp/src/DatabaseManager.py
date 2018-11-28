import uuid

from werkzeug.utils import secure_filename

from src.UserClass import UserClass
from redis import Redis

__db = Redis()
__db_table_users = "cholewp1:webapp:v4"
__db_table_sessions = "cholewp1:webapp:v4:session"
__db_table_user_file = "cholewp1:dl:v4:user_file"
__db_table_file = "cholewp1:dl:v4:file"


# FILE ACCESS
def check_file_count(user):
    file_ids = get_user_file_ids(user)
    if len(file_ids) > 4:
        return False
    return True


def get_new_file_id(user):
    if not check_file_count(user):
        return None
    __id = "file_" + str(uuid.uuid4()).replace("-", "X")
    db_rec = __db.hget(__db_table_file, __id)
    while db_rec is not None:
        __id = "file_" + str(uuid.uuid4()).replace("-", "X")
        db_rec = __db.hget(__db_table_file, __id)

    return __id


def get_file_name_by_id(__id):
    return __db.hget(__db_table_file, __id).decode('utf-8')


def save_user_file_to_db(user, file_id, filename):
    file_ids = get_user_file_ids(user)
    if len(file_ids) > 4:
        return None

    file_ids.add(file_id)

    __db.hset(__db_table_file, file_id, filename)
    __db.hset(__db_table_user_file, user, tuple(file_ids))

    return file_id


def __get_file_names_by_ids(ids):
    names = {}
    n_ids = set(ids)

    for __id in n_ids:
        filename = get_file_name_by_id(__id)
        if filename is not None:
            names[__id] = filename

    return names


def __byte_to_set(rec):
    txt = rec.decode('utf-8')
    txt = txt.replace("{", "")
    txt = txt.replace("}", "")
    txt = txt.replace("\'", "")
    txt = txt.replace(" ", "")
    txt = txt.replace("\"", "")
    txt = txt.replace("(", "")
    txt = txt.replace(")", "")
    return set(txt.split(","))


def get_user_file_ids(user):
    ids = __db.hget(__db_table_user_file, user)
    if ids is None:
        ids = set()
    else:
        ids = __byte_to_set(ids)

    return ids


def get_user_by_username(username):
    db_record = __db.hget(__db_table_users, username)
    if db_record is None:
        return None
    user = UserClass(db_record.decode('utf-8'))
    if user.username == username:
        return user

    return None


def get_user_file_names(user):
    ids = get_user_file_ids(user)
    files = __get_file_names_by_ids(ids)

    ret = '{\"files\":['
    flag = False
    for file_id in files.keys():
        if flag:
            ret = ret + ","
        else:
            flag = True

        ret = ret + '[ "' + file_id + '", "' + files[file_id] + '" ]'

    ret = ret + "]}"
    return ret


# USER AND SESSION ACCESS
def _add_user_to_db(user):
    db_user = get_user_by_username(user.username)
    if db_user is not None:
        return False
    else:
        dbrecord = user.to_dbrecord()
        __db.hset(__db_table_users, user.username, dbrecord)
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


def create_new_session(username):
    sid = str(uuid.uuid4())
    __db.hset(__db_table_sessions, username, sid)
    return sid


def check_session_valid(username, sid):
    dbsid = __db.hget(__db_table_sessions, username).decode('utf-8')
    if dbsid is None:
        return False
    if dbsid == sid:
        return True
    return False


def delete_session(sid):
    __db.hdel(__db_table_sessions, sid)


def init_db():
    __db.hset(__db_table_file, "file_61b14334X9c22X4308X8b6bX23069352d2d7", "t_1.txt")
    __db.hset(__db_table_file, "file_2533c38dXb1bdX4157X9ed0X4972ae37ac4f", "t.txt")
    __db.hset(__db_table_file, "file_f49e12b9X9eb5X43c6X82baXa17f4911dff9", "t2.txt")
    __db.hset(__db_table_user_file, "cholewp1", (
        "file_61b14334X9c22X4308X8b6bX23069352d2d7",
        "file_2533c38dXb1bdX4157X9ed0X4972ae37ac4f",
        "file_f49e12b9X9eb5X43c6X82baXa17f4911dff9"
    ))
