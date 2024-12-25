from bson import ObjectId
from app.core.db import get_db
from app.image.model import delete_image


def load_cards(data):
    """Upload group of cards"""
    all_success = True
    for item in data:
        try:
            response, status_code = load_card_to_db(item)
            if status_code != 200:
                all_success = False
        except Exception as e:
            all_success = False

    if all_success:
        return {"message": "All items loaded successfully."}, 200
    else:
        return response, status_code


def load_card_to_db(json_data):
    """Insert a card into the database"""
    db = get_db()
    collection = db['cards']
    try:
        if json_data.get("_id"):
            existing_card = collection.find_one({"_id": json_data.get("_id")})

            if existing_card:
                print(f"Card with _id {json_data.get('_id')}"
                      f" already exists. Skipping insertion.")
                return {"error": f"Card with the same _id already"
                                 f" exists: {json_data.get('_id')}, Skipped insertion"}, 200

            mark_unchecked(json_data)
            result = collection.insert_one(json_data)
            print(f"Data inserted with ID: {result.inserted_id}")

        return {"message": "Card successfully uploaded."}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500


def get_card_correctness(_id):
    """Retrieve the 'correct' field of a card from the database"""
    db = get_db()
    collection = db['cards']

    try:
        card = collection.find_one({"_id": ObjectId(_id)})
        if not card:
            return {"error": "Card not found."}, 404
        return int(card["correct"])
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500


def get_card_by_id(card_id):
    """Retrieve a card by its _id"""
    db = get_db()
    collection = db['cards']
    try:
        card = collection.find_one({"_id": ObjectId(card_id)})
        return card
    except Exception as e:
        print(f"Error getting card: {e}")
        return None


def update_card(card_id, data):
    """Update a card with new data"""
    db = get_db()
    collection = db['cards']
    try:
        collection.update_one({"_id": ObjectId(card_id)}, {"$set": data})
        return True
    except Exception as e:
        print(f"Error updating card: {e}")
        return False


def increment_correct(card_id, user_id):
    """Increment the 'correct' field for a card"""
    db = get_db()
    collection = db['cards']
    try:
        collection.update_one({"_id": ObjectId(card_id)},
                              {"$inc": {"correct": 1},
                               "$push": {"checked_by": user_id}})
        return True
    except Exception as e:
        print(f"Error incrementing 'correct' field: {e}")
        return False


def get_random_card(user_id):
    """Get a random card with 'correct' less than 2"""
    db = get_db()
    collection = db['cards']
    try:
        card = collection.find_one(
            {
                "correct": {"$lt": 2},
                "checked_by": {"$nin": [user_id]}
             },
            sort=[("correct", -1)]  # Sort by correctness in descending order
        )
        return card
    except Exception as e:
        print(f"Error getting random card: {e}")
        return None

def retrieve_validated_cards():
    db = get_db()
    collection = db['cards']
    cards = collection.find(
        {
            "correct": {"$gte": 2},
        }
    )
    return list(cards)


def mark_unchecked(data):
    """Mark the card as incorrect by setting its correctness to 0"""
    data['correct'] = 0
    data['checked_by'] = []


def find_card_by_image_code(card_image_code):
    db = get_db()
    collection = db['cards']
    try:
        card = collection.find_one({"image_code": card_image_code})
        if card:
            return card
        else:
            return {"error": "Card not found."}
    except Exception as e:
        print(f"Error finding card: {e}")
        return {"error": f"An error occurred: {str(e)}"}


def retrieve_all_image_codes_from_cards():
    db = get_db()
    collection = db['cards']
    image_codes = collection.find({}, {"image_code": 1, "_id": 0})
    return [card["image_code"] for card in image_codes]


def delete_card_by_image_code(card_image_code):
    db = get_db()
    collection = db['cards']
    try:
        result = collection.delete_one({"image_code": card_image_code})
        if result.deleted_count == 1:
            delete_image(card_image_code)
            return {"message": "Card successfully deleted."}, 200
        else:
            return {"error": "Card not found."}, 404
    except Exception as e:
        print(f"Error deleting card: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500
