
import bcrypt
from flask import request, jsonify, Blueprint
from app.card.model import load_cards
from app.image.model import load_images
from app.core.db import get_db


admin_bp = Blueprint('admin', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@admin_bp.route('/upload-data', methods=['POST'])
def upload_data():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": "No JSON data provided"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Invalid data type"}), 400

    try:
        response, status_code = load_cards(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500


@admin_bp.route('/upload-images', methods=['POST'])
def upload_image():
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    try:
        response, status_code = load_images(files)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500


@admin_bp.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400
    try:
        db = get_db()
        collection = db['users']
        login = data['login']

        existing_user = collection.find_one({"login": login})

        if existing_user:
            return jsonify({"message": "user with this login already exists"}), 400

        salt = bcrypt.gensalt()
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), salt)

        collection.insert_one(data)
        return {"message": "user added sucessfully!"}, 200
    except Exception as e:
        return jsonify({"message": f"Faild to add user: {str(e)}"}), 500




