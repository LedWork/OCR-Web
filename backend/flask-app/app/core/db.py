import os
from pymongo import MongoClient


def get_db():
    """Return a database connection to MongoDB"""
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER", "root"),
        password=os.getenv("MONGO_PASS", "pass"),
    )
    db = client["animal_db"]
    return db