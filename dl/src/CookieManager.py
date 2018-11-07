import json
from datetime import datetime, timedelta

import jwt

secret = b'soinGERG#25gappk2GWG32$#^ azg'


def validate_user_jwt(token, username):
    token = jwt.decode(token, secret, "HS256")
    expire = token['exp']
    if username != token['user']:
        return False

    return datetime.now() < datetime.fromtimestamp(expire)
