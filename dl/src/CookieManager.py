from datetime import datetime

import jwt

from src import ConfigManager

secret = ConfigManager.get_config("DL_COOKIE_SECRET_KEY")
secure = ConfigManager.get_config("APP_SECURE")


def validate_user_jwt(token, username):
    token = jwt.decode(token, secret, "HS256")
    expire = token['exp']
    if username != token['user']:
        return False

    return datetime.now() < datetime.fromtimestamp(expire)


def validate_file_by_jwt(token, file_id):
    token = jwt.decode(token, secret, "HS256")
    expire = token['exp']
    file_ids = token['file_list']

    if file_id not in file_ids:
        return False

    return datetime.now() < datetime.fromtimestamp(expire)
