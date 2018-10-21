import hashlib


class UserClass:
    __login_index = 0
    __hash_index = 1

    def __init__(self, db_record):
        user_atr = db_record.split()
        self._username = user_atr[self.__login_index]
        self._hash = user_atr[self.__hash_index]

    @property
    def username(self):
        return self._username

    @property
    def hash(self):
        return self._hash

    def check_password(self, password):
        passhash = hashlib.sha256(password.encode()).hexdigest()
        return self._hash == passhash

    def to_dbrecord(self):
        return self._username + " " + self._hash

    @classmethod
    def create_user(cls, username, password):
        passhash = hashlib.sha256(password.encode()).hexdigest()
        return cls(username + " " + passhash)
