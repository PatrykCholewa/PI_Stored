import uuid

from redis import Redis

from src import ConfigManager

__db = Redis()
__db_table_user_file = "cholewp1:dl:v4:user_file"
__db_table_file = "cholewp1:dl:v4:file"
__db_table_shared_file = "cholewp1:dl:v5:shared_file"

__sharelink_prefix = ConfigManager.get_config("WEBAPP_SHARELINK_PREFIX")


def check_file_count(user):
    file_ids = get_user_file_ids(user)
    if len(file_ids) > 5:
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
    s = __db.hget(__db_table_file, __id)
    try:
        return s.decode('utf-8')
    except Exception as e:
        print(e)
        return None


def save_user_file_to_db(user, file_id, filename):
    file_ids = get_user_file_ids(user)
    if len(file_ids) > 5:
        return False
    file_ids.add(file_id)

    __db.hset(__db_table_file, file_id, filename)
    __db.hset(__db_table_user_file, user, tuple(file_ids))

    return True


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


def get_user_file_names(user):
    ids = get_user_file_ids(user)

    files = []

    for __id in ids:
        name = get_file_name_by_id(__id)
        if name is None:
            __db.hdel(__db_table_file, __id)
            continue

        download = "../../../dl/file/" + __id + "/name/" + name
        sharelink = get_file_sharelink(__id)

        file = {
            'id': __id,
            'name': name,
            'download': download,
            'sharelink': sharelink
        }

        files.append(file)

    return files


def is_file_shared(file_id):
    res = __db.hget(__db_table_shared_file, file_id)
    if res is None:
        return False
    else:
        return True


def get_file_sharelink(file_id):
    if not is_file_shared(file_id):
        return ""

    return __db.hget(__db_table_shared_file, file_id).decode('utf-8')


def set_file_shared(file_id):
    __db.hset(__db_table_shared_file, file_id, __sharelink_prefix + file_id)


def init_db():
    __db.hset(__db_table_file, "file_61b14334X9c22X4308X8b6bX23069352d2d7", "t_1.txt")
    __db.hset(__db_table_file, "file_2533c38dXb1bdX4157X9ed0X4972ae37ac4f", "t.txt")
    __db.hset(__db_table_file, "file_f49e12b9X9eb5X43c6X82baXa17f4911dff9", "t2.txt")
    __db.hset(__db_table_user_file, "cholewp1", (
        "file_61b14334X9c22X4308X8b6bX23069352d2d7",
        "file_2533c38dXb1bdX4157X9ed0X4972ae37ac4f",
        "file_f49e12b9X9eb5X43c6X82baXa17f4911dff9"
    ))
