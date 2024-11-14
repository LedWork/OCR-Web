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
    db = client["main_db"]
    return db


def get_correct_cards():
    db = get_db()
    collection = db['cards']
    try:
        correct_cards = collection.find({"correct": True})
        return list(correct_cards)
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}
