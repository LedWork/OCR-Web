
from flask import jsonify, request, Blueprint, session
from .model import (get_card_by_id,
                    update_card,
                    increment_correct,
                    get_random_card)

from app.auth.decorators import login_required
from app.core.utils import parse_json

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

    if int(card.get("correct", 0)) >= 1:
        card.pop("correct", None)
        card.pop("_id", None)
        card.pop("checked_by", None)
        if card != data:
            data["correct"] = 0

    if update_card(card_id, data):
        increment_correct(card_id, user_id, 1)
        return jsonify({"message": "Card marked as correct and updated."}), 200
    else:
        return jsonify({"error": "Error updating card."}), 500


@card_bp.route("/random", methods=["GET"])
@login_required
def send_random_card():
    user_id = session.get('user')
    card = get_random_card(user_id)
    card.pop("checked_by")
    card.pop("correct")

    card = parse_json(card)
    if not card:
        return jsonify({"error": "No cards available in the database."}), 400

    return jsonify(card), 200
