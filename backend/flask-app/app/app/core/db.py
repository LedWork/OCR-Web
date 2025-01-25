from pymongo import MongoClient
import os


def get_db():
    """Return a database connection to MongoDB"""
    try:
        client = MongoClient(
            host=os.getenv("MONGO_HOST", "mongodb"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "root"),
            password=os.getenv("MONGO_PASS", "pass"),
        )
        db = client["main_db"]
        return db
    except Exception as e:
        raise
