import base64
import random

from flask import jsonify, request, Blueprint

from app.core.db import get_db
from app.core.mark_data import mark_correct
from app.core.utils import parse_json

card_bp = Blueprint('card', __name__)


@card_bp.route('/correct-card', methods=['POST'])
def receive_correct_card():
    data = request.get_json()
    if data is None:
        return 400
    db = get_db()
    collection = db['cards']
    card = collection.find({"_id": data['_id']})
    if not card:
        return jsonify({"error": "No such a card in db"}), 404
    mark_correct(data)
    try:
        collection.delete_one({"_id": data['_id']})
        collection.insert_one(data)
        print(data)
        return jsonify({"message": "Card marked as correct and updated."}), 200
    except Exception as e:
        print(f"An error occurred: {e}")


@card_bp.route('/random-card', methods=['GET'])
def send_random_card():
    db = get_db()
    collection = db['cards']

    cards = list(collection.find({"correct": False}))

    if not cards:
        return jsonify({"error": "No cards available in the database."}), 400

    random_card = random.choice(cards)

    random_card['_id'] = str(random_card['_id'])

    return jsonify(random_card), 200

@card_bp.route('/photo/<image_code>', methods=['GET'])
def send_photo(image_code):
    db = get_db()
    collection = db['images']

    try:
        image_data = list(collection.find({"_id": image_code}))
        if not image_data:
            return jsonify({"error": "No such a card in db"}), 400

        image_data = parse_json(image_data)
        return jsonify(image_data), 200
    except Exception as e:
         print(f"An error occurred: {e}")
         return jsonify({"error": f"An error occurred: {str(e)}"}), 500
