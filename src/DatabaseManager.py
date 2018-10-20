from src.UserClass import UserClass

__users_file = "db/users.db.txt"


def get_user_by_username(username):
    users = open(__users_file, "r").read().splitlines()
    for db_record in users:
        user = UserClass(db_record)
        if user.username == username:
            return user

    return None
