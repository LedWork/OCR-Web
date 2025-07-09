import datetime
import string
import random
import bcrypt
from app.core.db import get_db
from app import mail
from flask_mail import Message


def password_generator(length=10, symbols=False):
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

    data['password'] = ''
    data['is_super_user'] = False
    data['is_revoked'] = False
    data['created_at'] = datetime.datetime.now()
    collection.insert_one(data)

def generate_user_password(login):
    db = get_db()
    collection = db['users']
    user = collection.find_one({'login': login})

    if user is None:
        return False

    email = user['login']
    password = password_generator()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    collection.update_one(
        {'login': login},
        {'$set': {'password': hashed_password, 'created_at': datetime.datetime.now()}}
    )

    send_password_mail(email, password)

    return True

def send_password_mail(email, password):
    msg = Message(
        subject='Hasło do konta w programie OCR-PCK.',
        sender=mail.default_sender,
        recipients=[email]
    )
    msg.body = f"""
                Szanowni Państwo,
                
                Witamy serdecznie w naszym programie! Dziękujemy za dołączenie i udział. Z radością informujemy, że hasło do Twojego konta zostało utworzone.
                
                Hasło: {password}
                
                Prosimy o zachowanie tego hasła w bezpiecznym miejscu. W razie jakichkolwiek pytań lub wątpliwości, prosimy o kontakt.
                
                Z poważaniem,
                Zespół OCR-PCK
                """

    mail.send(msg)


def get_all_users():
    """Get all users from the database"""
    db = get_db()
    collection = db['users']
    users = list(collection.find({}, {'password': 0}))  # Exclude password field
    
    # Convert ObjectId to string for JSON serialization
    for user in users:
        if '_id' in user:
            user['_id'] = str(user['_id'])
    
    return users


def delete_user(login):
    """Delete a user by login"""
    db = get_db()
    collection = db['users']
    result = collection.delete_one({"login": login})
    return result.deleted_count > 0

def revoke_user(login):
    """Revoke a user by login - sets is_revoked to True instead of deleting"""
    db = get_db()
    collection = db['users']
    result = collection.update_one(
        {"login": login},
        {"$set": {"is_revoked": True}}
    )
    return result.modified_count > 0

def unrevoke_user(login):
    """Unrevoke a user by login - sets is_revoked to False"""
    db = get_db()
    collection = db['users']
    result = collection.update_one(
        {"login": login},
        {"$set": {"is_revoked": False}}
    )
    return result.modified_count > 0
