import hashlib
import string
import random
from os import urandom


class UserClass:
    __login_index = 0
    __hash_index = 1
    __salt_index = 2

    def __init__(self, db_record):
        user_atr = db_record.split()
        self._username = user_atr[self.__login_index]
        self._hash = user_atr[self.__hash_index]
        self._salt = user_atr[self.__salt_index]

    @property
    def username(self):
        return self._username

    @property
    def hash(self):
        return self._hash

    def check_password(self, password):
        passhash = hashlib.sha256((password + self._salt).encode()).hexdigest()
        return self._hash == passhash

    def to_dbrecord(self):
        return self._username + " " + self._hash + " " + self._salt

    @classmethod
    def create_user(cls, username, password):
        letters = string.ascii_lowercase
        salt = ''.join(random.choice(letters) for i in range(8))
        passhash = hashlib.sha256((password + salt).encode()).hexdigest()
        return cls(username + " " + passhash + " " + salt)
