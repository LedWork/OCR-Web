
from flask import jsonify, request, Blueprint, session
from .model import (get_card_by_id,
                    update_card,
                    increment_correct,
                    get_random_card)

from app.auth.decorators import login_required
from app.core.utils import parse_json
from app.core.db import get_db
from bson import ObjectId

card_bp = Blueprint("card", __name__)



@card_bp.route("/correct", methods=["POST"])
@login_required
def receive_correct_card():
    user_id = session.get('user')
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    card_id = data.get('_id')
    if not card_id:
        return jsonify({"error": "No card ID provided"}), 400

    card = get_card_by_id(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    data.pop("correct", None)
    data.pop("_id", None)
    data.pop("checked_by", None)

    # Check if user has already checked this card
    checked_by = card.get("checked_by", [])
    if user_id in checked_by:
        return jsonify({"error": "You have already checked this card."}), 400
    
    # Check if data is being changed (excluding system fields)
    card_data_for_comparison = {k: v for k, v in card.items() 
                               if k not in ['_id', 'correct', 'checked_by', 'created_at', 'updated_at']}
    data_for_comparison = {k: v for k, v in data.items() 
                          if k not in ['_id', 'correct', 'checked_by', 'created_at', 'updated_at']}
    
    data_changed = card_data_for_comparison != data_for_comparison
    
    # Determine if we should increment the correct field
    # Only increment if no data was changed, or if this is the first check
    should_increment = not data_changed or len(checked_by) == 0

    if update_card(card_id, data):
        if should_increment:
            increment_correct(card_id, user_id, 1)
            return jsonify({"message": "Card marked as correct and updated."}), 200
        else:
            # Add user to checked_by but don't increment correct field
            db = get_db()
            collection = db['cards']
            collection.update_one(
                {"_id": ObjectId(card_id)},
                {"$push": {"checked_by": user_id}}
            )
            return jsonify({"message": "Card updated but correct count not incremented due to data changes."}), 200
    else:
        return jsonify({"error": "Error updating card."}), 500


@card_bp.route("/random", methods=["GET"])
@login_required
def send_random_card():
    user_id = session.get('user')
    card = get_random_card(user_id)
    
    if not card:
        return jsonify({"error": "No cards available in the database."}), 400
    
    card.pop("checked_by", None)
    card.pop("correct", None)

    card = parse_json(card)
    if not card:
        return jsonify({"error": "No cards available in the database."}), 400

    return jsonify(card), 200
