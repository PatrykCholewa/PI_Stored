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


def __create_timestamp_past_5_minutes():
    expire = datetime.now()
    expire = expire + timedelta(minutes=5)
    return expire


def set_user_cookie_to_response(response, username):
    expire = __create_timestamp_past_5_minutes()

    new_response = response
    new_response.set_cookie(
        "user",
        __create_user_jwt(username, expire),
        max_age=300,
        expires=expire,
        path="/cholewp1/dl/",
        secure=False,
        httponly=True
    )
    return new_response
