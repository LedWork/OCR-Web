import logging
from bson import ObjectId
from datetime import datetime, timezone
from app.core.db import get_db
from app.core.utils import EXPECTED_CHECKS_PER_CARD
from app.image.model import delete_image

# Configure logging
logger = logging.getLogger(__name__)


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
        if json_data.get("image_code"):
            existing_card = collection.find_one({"image_code": json_data.get("image_code")})

            if existing_card:
                if existing_card.get('correct', 0) > 0:
                    return {
                        "error": f"Card with the same image code already exists: "
                                 f"and was checked already. Skipped insertion"}, 200
                else:
                    # Update existing card with new data and updated timestamp
                    update_data = json_data.copy()
                    update_data['updated_at'] = datetime.now(timezone.utc)
                    
                    db.collection.update_one(
                        {'_id': ObjectId(existing_card['_id'])},
                        {'$set': update_data}
                    )
                    return {"message": f"Card with _id {json_data.get('image_code')} was updated with new data."}, 200

            # Add timestamps for new card
            json_data['created_at'] = datetime.now(timezone.utc)
            json_data['updated_at'] = datetime.now(timezone.utc)
            
            mark_unchecked(json_data)
            result = collection.insert_one(json_data)
            print(f"Data inserted with ID: {result.inserted_id}")
            return {"message": "Card successfully uploaded."}, 200
        else:
            return {"error": "no image_code found"}, 400
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
        # Add updated timestamp
        data['updated_at'] = datetime.now(timezone.utc)
        collection.update_one({"_id": ObjectId(card_id)}, {"$set": data})
        return True
    except Exception as e:
        print(f"Error updating card: {e}")
        return False


def increment_correct(card_id, user_id, number):
    """Increment the 'correct' field for a card"""
    db = get_db()
    collection = db['cards']
    try:
        collection.update_one({"_id": ObjectId(card_id)},
                              {"$inc": {"correct": number},
                               "$push": {"checked_by": user_id}})
        return True
    except Exception as e:
        print(f"Error incrementing 'correct' field: {e}")
        return False


def get_random_card(user_id):
    """Get a random card with 'correct' less than EXPECTED_CHECKS_PER_CARD"""
    db = get_db()
    collection = db['cards']
    try:
        # Use MongoDB's $sample aggregation to get a random card efficiently
        pipeline = [
            {
                "$match": {
                    "correct": {"$lt": EXPECTED_CHECKS_PER_CARD},
                    "checked_by": {"$nin": [user_id]}
                }
            },
            {
                "$sample": {"size": 1}
            }
        ]
        
        result = list(collection.aggregate(pipeline))
        
        # Return the random card if found, otherwise None
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting random card: {e}")
        return None

def retrieve_validated_cards():
    logger.info("Starting retrieve_validated_cards function")
    db = get_db()
    collection = db['cards']
    
    # Log the query we're about to execute
    query = {"correct": {"$gte": EXPECTED_CHECKS_PER_CARD}}
    logger.info(f"Executing query: {query}")
    
    # Get total count of all cards for comparison
    total_cards = collection.count_documents({})
    logger.info(f"Total cards in database: {total_cards}")
    
    # Get count of validated cards
    validated_count = collection.count_documents(query)
    logger.info(f"Cards matching validation criteria: {validated_count}")
    
    cards = collection.find(query)
    cards_list = list(cards)
    logger.info(f"Retrieved {len(cards_list)} validated cards")
    
    logger.info("Completed retrieve_validated_cards function")
    return cards_list


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
    cards = collection.find({}, {"image_code": 1, "correct": 1, "checked_by": 1, "created_at": 1, "updated_at": 1, "_id": 0})
    
    # Expected number of checks per card (from the system configuration)
    
    cards_list = []
    for card in cards:
        current_checks = card.get('correct', 0)
        checked_by = card.get('checked_by', [])
        
        # Determine if card is fully validated or checked by admin
        is_validated = current_checks >= EXPECTED_CHECKS_PER_CARD
        is_admin_checked = 'admin' in checked_by
        
        # Determine color based on validation status
        is_green = is_validated or is_admin_checked
        
        # Ensure dates are properly formatted
        created_at = card.get("created_at")
        updated_at = card.get("updated_at")
        
        # Debug: print date types for troubleshooting
        print(f"Card {card.get('image_code')}: created_at type: {type(created_at)}, value: {created_at}")
        print(f"Card {card.get('image_code')}: updated_at type: {type(updated_at)}, value: {updated_at}")
        
        # Convert BSON dates to ISO format strings if they exist
        if created_at:
            if hasattr(created_at, 'isoformat'):
                # Ensure it's in UTC and format as ISO string
                if created_at.tzinfo is None:
                    # If no timezone info, assume it's UTC
                    created_at = created_at.replace(tzinfo=timezone.utc)
                created_at = created_at.isoformat()
            elif isinstance(created_at, dict) and '$date' in created_at:
                # Handle BSON date objects - convert to ISO string
                # The $date field contains an ISO string, so we can use it directly
                created_at = created_at['$date']
            else:
                # Fallback: try to convert to string
                created_at = str(created_at)
        
        if updated_at:
            if hasattr(updated_at, 'isoformat'):
                # Ensure it's in UTC and format as ISO string
                if updated_at.tzinfo is None:
                    # If no timezone info, assume it's UTC
                    updated_at = updated_at.replace(tzinfo=timezone.utc)
                updated_at = updated_at.isoformat()
            elif isinstance(updated_at, dict) and '$date' in updated_at:
                # Handle BSON date objects - convert to ISO string
                # The $date field contains an ISO string, so we can use it directly
                updated_at = updated_at['$date']
            else:
                # Fallback: try to convert to string
                updated_at = str(updated_at)
        
        cards_list.append({
            "image_code": card["image_code"],
            "check_status": f"[{current_checks}/{EXPECTED_CHECKS_PER_CARD}]",
            "is_green": is_green,
            "current_checks": current_checks,
            "expected_checks": EXPECTED_CHECKS_PER_CARD,
            "created_at": created_at,
            "updated_at": updated_at
        })
    
    return cards_list


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
