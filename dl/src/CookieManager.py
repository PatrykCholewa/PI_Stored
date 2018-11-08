import json
from datetime import datetime, timedelta

import jwt

secret = b'soinGERG#25gappk2GWG32$#^ azg'
secure = False


def __create_file_jwt(file_list, expire):

    encode = jwt.encode(
        {
            "file_list": tuple(file_list),
            "exp": expire.timestamp()
        }, secret, "HS256")
    return encode


def set_user_cookie_to_response(response, file_list):
    expire = datetime.now()
    expire = expire + timedelta(minutes=2)

    new_response = response
    new_response.set_cookie(
        "file",
        __create_file_jwt(file_list, expire),
        max_age=120,
        expires=expire,
        path="/cholewp1/dl/",
        secure=secure,
        httponly=True
    )
    return new_response


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
