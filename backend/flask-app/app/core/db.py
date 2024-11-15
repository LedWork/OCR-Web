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


def load_card_to_db(json_data):
    db = get_db()
    collection = db['cards']
    try:
        if json_data.get("_id"):
            existing_card = collection.find_one({"_id": json_data.get("_id")})

            if existing_card:
                print(f"Card with _id {json_data.get('_id')} already "
                      f"exists. Skipping insertion.")
                return {"error": f"Card with the same _id already "
                                 f"exists: {json_data.get('_id')}"}, 400

        mark_unchecked(json_data)
        result = collection.insert_one(json_data)
        print(f"Data inserted with ID: {result.inserted_id}")

        return {"message": "Card successfully uploaded."}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500


def get_card_correctness(_id):
    db = get_db()
    collection = db['cards']

    card = collection.find_one({"_id": _id})

    if not card:
        return {"error": "Card not found."}

    return int(card["correct"])


def mark_checked(data):
    correct_num = get_card_correctness(data["_id"])
    data['correct'] = int(correct_num) + 1
    print(data)
    print(f"Marked as correct: {data}")


def mark_unchecked(data):
    data['correct'] = 0
