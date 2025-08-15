import datetime
import string
import random
import bcrypt
import logging
from app.core.db import get_db
from app import mail
from flask_mail import Message
from flask import current_app

logger = logging.getLogger(__name__)

def password_generator(length=10, symbols=False):
    logger.info(f"Generating password with length={length}, symbols={symbols}")
    characters = string.ascii_letters + string.digits
    if symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def user_exists(data):
    logger.info(f"Checking if user exists with data: {data}")
    db = get_db()
    collection = db['users']
    login = data['login']
    logger.info(f"Looking for user with login: {login}")

    existing_user = collection.find_one({"login": login})
    exists = existing_user is not None
    logger.info(f"User with login '{login}' exists: {exists}")
    return exists


def create_user(data):
    logger.info(f"Creating user with data: {data}")
    db = get_db()
    collection = db['users']

    data['password'] = ''
    data['is_super_user'] = False
    data['is_revoked'] = False
    data['created_at'] = datetime.datetime.now()
    
    logger.info(f"Inserting user with prepared data: {data}")
    result = collection.insert_one(data)
    logger.info(f"User created successfully with ID: {result.inserted_id}")
    return result.inserted_id

def generate_user_password(login):
    logger.info(f"Generating password for user with login: {login}")
    db = get_db()
    collection = db['users']
    user = collection.find_one({'login': login})

    if user is None:
        logger.warning(f"User with login '{login}' not found")
        return False

    logger.info(f"Found user: {user.get('login')} (ID: {user.get('_id')})")
    email = user['login']
    password = password_generator()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    logger.info(f"Password hashed successfully")

    update_result = collection.update_one(
        {'login': login},
        {'$set': {'password': hashed_password, 'created_at': datetime.datetime.now()}}
    )
    logger.info(f"Password updated in database. Modified count: {update_result.modified_count}")

    return send_password_mail(email, password)

def send_password_mail(email, password):
    try:
        logger.info(f"Attempting to send password email to: {email}")
        
        # Check if mail configuration is properly set
        if not mail.app.config.get('MAIL_SERVER'):
            logger.error("MAIL_SERVER not configured")
            return False
            
        if not mail.app.config.get('MAIL_USERNAME'):
            logger.error("MAIL_USERNAME not configured")
            return False
            
        if not mail.app.config.get('MAIL_PASSWORD'):
            logger.error("MAIL_PASSWORD not configured")
            return False

        # Get password validity time from config
        password_validity_minutes = current_app.config.get('PASSWORD_VALIDITY_MINUTES', 10)
        validity_hours = password_validity_minutes // 60
        validity_minutes = password_validity_minutes % 60
        
        # Format validity time for display
        if validity_hours > 0 and validity_minutes > 0:
            validity_text = f"{validity_hours} godzin i {validity_minutes} minut"
        elif validity_hours > 0:
            validity_text = f"{validity_hours} godzin"
        else:
            validity_text = f"{validity_minutes} minut"

        msg = Message(
            subject='Hasło do konta w programie OCR-PCK.',
            sender=mail.default_sender,
            recipients=[email]
        )
        msg.body = f"""
                    Szanowni Państwo,
                    
                    Witamy serdecznie w naszym programie! Dziękujemy za dołączenie i udział. Z radością informujemy, że hasło do Państwa konta zostało utworzone.
                    
                    Hasło: {password}

                    Hasło będzie ważne przez {validity_text}. Po tym czasie będzie trzeba wygenerować nowe hasło.
                    Prosimy o zachowanie tego hasła w bezpiecznym miejscu. W razie jakichkolwiek pytań lub wątpliwości, prosimy o kontakt.
                    
                    Z poważaniem,
                    Zespół OCR-PCK
                    """

        logger.info(f"Preparing to send email to {email}")
        mail.send(msg)
        logger.info(f"Password email sent successfully to: {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password email to {email}: {str(e)}")
        logger.error(f"Mail configuration - Server: {mail.app.config.get('MAIL_SERVER')}, "
                    f"Port: {mail.app.config.get('MAIL_PORT')}, "
                    f"Username: {mail.app.config.get('MAIL_USERNAME')}")
        return False


def get_all_users():
    """Get all users from the database"""
    logger.info("Retrieving all users from database")
    db = get_db()
    collection = db['users']
    users = list(collection.find({}, {'password': 0}))  # Exclude password field
    logger.info(f"Found {len(users)} users in database")
    
    # Convert ObjectId to string for JSON serialization
    for user in users:
        if '_id' in user:
            user['_id'] = str(user['_id'])
    
    logger.info(f"Returning {len(users)} users with IDs converted to strings")
    return users



def revoke_user(login):
    """Revoke a user by login - sets is_revoked to True instead of deleting"""
    logger.info(f"Attempting to revoke user with login: {login}")
    db = get_db()
    collection = db['users']
    
    # First check if user exists
    existing_user = collection.find_one({"login": login})
    if existing_user is None:
        logger.warning(f"User with login '{login}' not found for revocation")
        return False
    
    logger.info(f"Found user to revoke: {existing_user.get('login')} (ID: {existing_user.get('_id')})")
    result = collection.update_one(
        {"login": login},
        {"$set": {"is_revoked": True}}
    )
    revoked = result.modified_count > 0
    logger.info(f"User revocation result: {revoked} (modified count: {result.modified_count})")
    return revoked

def unrevoke_user(login):
    """Unrevoke a user by login - sets is_revoked to False"""
    logger.info(f"Attempting to unrevoke user with login: {login}")
    db = get_db()
    collection = db['users']
    
    # First check if user exists
    existing_user = collection.find_one({"login": login})
    if existing_user is None:
        logger.warning(f"User with login '{login}' not found for unrevocation")
        return False
    
    logger.info(f"Found user to unrevoke: {existing_user.get('login')} (ID: {existing_user.get('_id')})")
    result = collection.update_one(
        {"login": login},
        {"$set": {"is_revoked": False}}
    )
    unrevoked = result.modified_count > 0
    logger.info(f"User unrevocation result: {unrevoked} (modified count: {result.modified_count})")
    return unrevoked
