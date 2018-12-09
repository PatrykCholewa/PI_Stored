import json


def __load_config():
    __f_tmp = open(__config_file_path)
    __d = json.load(__f_tmp)
    __f_tmp.close()
    return __d


__config_file_path = "../utils/config/webapp.json"
__config_dict = __load_config()


def get_config(key):
    return __config_dict[key]
