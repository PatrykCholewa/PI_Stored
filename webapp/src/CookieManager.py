from datetime import datetime, timedelta

import jwt

secret = b'soinGERG#25gappk2GWG32$#^ azg'


def __create_user_jwt(username, expire):
    encode = jwt.encode(
        {
            "user": username,
            "exp": expire.timestamp()
        }, secret, "HS256")
    return encode


def __create_user_file_jwt(username, path, expire):
    encode = jwt.encode(
        {
            "user": username,
            "file": path,
            "exp": expire.timestamp()
        }, secret, "HS256")
    return encode


def set_user_cookie_to_response(response, username):
    expire = datetime.now()
    expire = expire + timedelta(minutes=5)

    new_response = response
    new_response.set_cookie(
        "user",
        __create_user_jwt(username, expire),
        max_age=300,
        expires=expire,
        path="/cholewp1/dl/",
        secure=True,
        httponly=True
    )
    return new_response
