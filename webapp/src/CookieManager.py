from datetime import datetime, timedelta

import jwt

dl_secret = b'soinGERG#25gappk2GWG32$#^ azg'
event_secret = "ouwejgiq43q=V$Q:Q$23guj92:[;qg"
secure = True


def __create_file_jwt(file_list, expire):
    encode = jwt.encode(
        {
            "file_list": tuple(file_list),
            "exp": expire.timestamp()
        }, dl_secret, "HS256")
    return encode


def set_file_cookie_to_response(response, file_list):
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


def __create_events_jwt(username, expire):
    encode = jwt.encode(
        {
            "username": username,
            "exp": expire.timestamp()
        }, event_secret, "HS256")
    return encode


def set_events_jwt_to_response(response, username):
    expire = datetime.now()
    expire = expire + timedelta(minutes=2)

    new_response = response
    new_response.set_cookie(
        "events",
        __create_events_jwt(username, expire),
        max_age=120,
        expires=expire,
        path="/events/",
        secure=secure,
        httponly=True
    )
    return new_response
