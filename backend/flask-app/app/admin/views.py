import bcrypt
from flask import request, jsonify, Blueprint


from app.core.db import get_db
from app.core.mark_data import mark_incorrect
from app.core.db import load_card_to_db
from app.image.model import load_image_to_db


admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@admin_bp.route('/upload-data', methods=['PUT'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        response, status_code = load_card_to_db(data)
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

@admin_bp.route('/upload-image/<image_code>', methods=['POST'])
def upload_image(image_code):
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type or no file selected"}), 415

    try:
        response, status_code = load_image_to_db(file, image_code)
        return jsonify(response), status_code
    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500

