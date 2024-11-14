from pymongo import MongoClient
import os
import json
import base64

from app.core.mark_data import mark_incorrect


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
                print(f"Card with _id {json_data.get('_id')} already exists. Skipping insertion.")
                return {"error": f"Card with the same _id already exists: {json_data.get('_id')}"}, 400

        mark_incorrect(json_data)
        result = collection.insert_one(json_data)
        print(f"Data inserted with ID: {result.inserted_id}")

        return {"message": "Card successfully uploaded."}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500

def load_image_to_db(file, image_code):
    db = get_db()
    collection = db['images']

    try:
        existing_image = collection.find_one({"_id": image_code})

        if existing_image:
            print(f"Image with _id {image_code} already exists. Skipping insertion.")
            return {"error": f"Image with the same _id already exists: {image_code}"}, 400

        file_content = file.read()
        photo_data = base64.b64encode(file_content).decode('utf-8')

        collection.insert_one({ "_id": image_code,"photo": photo_data})

        return {"message": "Photo successfully uploaded and linked to the card"}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_correct_cards():
    db = get_db()
    collection = db['cards']
    try:
        correct_cards = collection.find({"correct": True})
        return list(correct_cards)
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}
