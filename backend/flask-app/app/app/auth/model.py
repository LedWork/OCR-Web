import datetime

from bcrypt import checkpw
from app.core.db import get_db
from flask import current_app


def user_exists(login):
    db = get_db()
    collection = db['users']
    # Normalize email to lowercase for case-insensitive lookup
    user = collection.find_one({"login": login.lower()})
    if user is not None:
        return True
    else:
        return False


def password_correct(login, password):
    db = get_db()
    collection = db['users']
    # Normalize email to lowercase for case-insensitive lookup
    user = collection.find_one({"login": login.lower()})

    if user is None:
        return False

    if checkpw(password.encode('utf-8'), user['password']):
        return True
    else:
        return False

def has_password_expired(login):
    db = get_db()
    collection = db['users']
    # Normalize email to lowercase for case-insensitive lookup
    user = collection.find_one({"login": login.lower()})

    if user is None:
        return False

    if user['is_super_user']:
        return False

    user_created_at = user['created_at']

    current_time = datetime.datetime.now()
    time_difference = current_time - user_created_at

    # Get configurable password validity from app config
    password_validity_minutes = current_app.config.get('PASSWORD_VALIDITY_MINUTES', 10)
    validity_timedelta = datetime.timedelta(minutes=password_validity_minutes)

    if time_difference >= validity_timedelta:
        # Normalize email to lowercase for update as well
        collection.update_one(
            {"login": login.lower()},
            {"$unset": {"password": ""}})
        return True
    else:
        return False

def is_admin(login):
    db = get_db()
    collection = db['users']
    # Normalize email to lowercase for case-insensitive lookup
    user = collection.find_one({"login": login.lower()})

    if user is None:
        return False

    return user.get('is_super_user', False)

def is_user_revoked(login):
    """Check if a user is revoked"""
    db = get_db()
    collection = db['users']
    # Normalize email to lowercase for case-insensitive lookup
    user = collection.find_one({"login": login.lower()})
    return user is not None and user.get('is_revoked', False)