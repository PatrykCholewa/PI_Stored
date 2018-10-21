from os import listdir, mkdir

__users_dir = "db/userfiles/"


def check_dir_exist(username):
    dirs = listdir(__users_dir)
    for __dir in dirs:
        if __dir == username:
            return

    return mkdir(__users_dir + username)


def get_user_file_names(username):
    check_dir_exist(username)
    files = listdir(__users_dir + username)
    ret = '{\"files\":['
    flag = False
    for file in files:
        if flag:
            ret = ret + ","
        else:
            flag = True

        ret = ret + '"' + file + '"'

    ret = ret + "]}"
    return ret
