import uuid

from redis import Redis
from werkzeug.utils import secure_filename

__users_dir = "db/userfiles/"

__db = Redis()
__db_table_user_file = "cholewp1:dl:v4:user_file"
__db_table_file = "cholewp1:dl:v4:file"


def __get_new_file_id():
    __id = "file_" + str(uuid.uuid4()).replace("-", "X")
    db_rec = __db.hget(__db_table_file, __id)
    while db_rec is not None:
        __id = "file_" + str(uuid.uuid4()).replace("-", "X")
        db_rec = __db.hget(__db_table_file, __id)

    return __id


def __get_file_names_by_ids(ids):
    names = set()
    n_ids = set(ids)

    for __id in n_ids:
        filename = __db.hget(__db_table_file, __id)
        if filename is not None:
            names.add(filename)

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
    ids = __byte_to_set(ids)
    if ids is None:
        ids = set()

    return ids


def get_user_file_names(user):
    ids = get_user_file_ids(user)
    filenames = __get_file_names_by_ids(ids)

    ret = '{\"files\":['
    flag = False
    for file in filenames:
        if flag:
            ret = ret + ","
        else:
            flag = True

        ret = ret + '"' + file.decode('utf-8') + '"'

    ret = ret + "]}"
    return ret


def get_file(file_id):
    file = open(__users_dir + file_id, "rb")
    if file is None:
        return None

    return file


def save_user_file(user, file):
    file_ids = get_user_file_ids(user)
    if len(file_ids) > 4:
        return False

    filename = secure_filename(file.filename)

    new_id = __get_new_file_id()
    file.save(__users_dir + new_id)

    file_ids.add(new_id)

    __db.hset(__db_table_file, new_id, filename)
    __db.hset(__db_table_user_file, user, tuple(file_ids))

    return True
