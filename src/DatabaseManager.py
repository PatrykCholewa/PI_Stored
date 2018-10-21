from src.UserClass import UserClass

__users_file = "db/users.db.txt"


def get_user_by_username(username):
    users = open(__users_file, "r").read().splitlines()
    for db_record in users:
        user = UserClass(db_record)
        if user.username == username:
            return user

    return None


def _add_user_to_db(user):
    db_user = get_user_by_username(user.username)
    if db_user is not None:
        return False
    else:
        file = open(__users_file, "r")
        filetext = file.read()
        file.close()
        filetext = filetext + "\n" + user.to_dbrecord()
        file = open(__users_file, "w")
        file.write(filetext)
        return True


def add_new_user(username, password):
    user = UserClass.create_user(username, password)
    if _add_user_to_db(user):
        return user
    else:
        return None


def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user.check_password(password):
        return True
    else:
        return False
