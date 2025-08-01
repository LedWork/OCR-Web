from pymongo import MongoClient
import os
import bcrypt

def ensure_admin_user(db):
    users = db["users"]
    admin_login = os.getenv("ADMIN_LOGIN")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # Check if admin user already exists
    existing_admin = users.find_one({"login": admin_login, "is_super_user": True})
    
    if existing_admin is None:
        # Only create admin user if it doesn't exist
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(admin_password.encode("utf-8"), salt)
        users.insert_one({
            "login": admin_login,
            "password": hashed_password,
            "is_super_user": True
        })
        print(f"Admin user '{admin_login}' created successfully")
    else:
        print(f"Admin user '{admin_login}' already exists, skipping creation")

def get_db():
    """Return a database connection to MongoDB"""
    try:
        client = MongoClient(
            host=os.getenv("MONGO_HOST", "mongodb"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER"),
            password=os.getenv("MONGO_PASS"),
        )
        db = client["main_db"]

        return db
    except Exception as e:
        raise
