import string
import random
import bcrypt
from app.core.db import get_db


def password_generator(length=8, symbols=True):
    characters = string.ascii_letters + string.digits
    if symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def user_exists(data):
    db = get_db()
    collection = db['users']
    login = data['login']

    existing_user = collection.find_one({"login": login})
    return existing_user is not None


def create_user(data):
    db = get_db()
    collection = db['users']

    password = password_generator()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    data['password'] = hashed_password
    data['is_super_user'] = True

    collection.insert_one(data)
    return password
