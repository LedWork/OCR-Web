from bcrypt import checkpw
from app.core.db import get_db


def user_exists(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})
    if user is not None:
        return True
    else:
        return False


def password_correct(login, password):
    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": login})

    if checkpw(password.encode('utf-8'), user['password']):
        return True
    else:
        return False
