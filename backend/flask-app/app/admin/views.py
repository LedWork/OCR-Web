from flask import request, jsonify, Blueprint
from app.card.model import load_cards
from app.image.model import load_images
from app.admin.model import create_user, user_exists
from app.auth.decorators import admin_required


admin_bp = Blueprint('admin', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@admin_bp.route('/upload-data', methods=['POST'])
@admin_required
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
@admin_required
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
@admin_required
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400
    try:
        if user_exists(data):
            return jsonify({"message": "user with this login already exists"}), 400

        password = create_user(data)
        return {"message": f"user added sucessfully!", "password": password}, 200
    except Exception as e:
        return jsonify({"message": f"Failed to add user: {str(e)}"}), 500


# TEMPORARY FOR TESTING, WILL BE DELETED IN PROD VERSION
from app.core.db import get_db
import bcrypt
@admin_bp.route('/temp-admin', methods=['POST'])
def create_temp_admin():
    db = get_db()
    collection = db['users']

    data = request.get_json()

    password = 'admin'
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    data['login'] = 'admin'
    data['password'] = hashed_password
    data['is_super_user'] = True

    collection.insert_one(data)
    return {"message": f"Admin created! Login: admin Password: admin"}, 200