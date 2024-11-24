from flask import request, jsonify, Blueprint

from app.core.db import load_card_to_db
from app.image.model import load_image_to_db

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route('/upload-data', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        response, status_code = load_card_to_db(data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"Failed to load data: {str(e)}"}), 500

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