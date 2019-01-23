from datetime import datetime, timedelta
from src import ConfigManager


import jwt

dl_secret = ConfigManager.get_config("DL_COOKIE_SECRET_KEY")
event_secret = ConfigManager.get_config("EVENT_COOKIE_SECRET_KEY")
secure = ConfigManager.get_config("APP_SECURE")


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
