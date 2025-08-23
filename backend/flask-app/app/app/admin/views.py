from flask import request, jsonify, Blueprint
from app.card.model import (load_cards, find_card_by_image_code, delete_card_by_image_code,
                            retrieve_all_image_codes_from_cards)
from app.image.model import load_images
from app.admin.model import create_user, user_exists, get_all_users, revoke_user, unrevoke_user
from app.auth.decorators import admin_required
from app.core.utils import parse_json, EXPECTED_CHECKS_PER_CARD
from app.card.model import (get_card_by_id, update_card, increment_correct)

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


@admin_bp.route('/upload-images-chunked', methods=['POST'])
@admin_required
def upload_images_chunked():
    """Handle chunked image uploads to avoid server limits"""
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files provided"}), 400

    # Get chunk metadata
    chunk_index = request.form.get('chunk_index', '0')
    total_chunks = request.form.get('total_chunks', '1')
    is_chunked = request.form.get('is_chunked', 'false')
    
    try:
        # Process this chunk of images
        response, status_code = load_images(files)
        
        # Add chunk information to response
        if isinstance(response, dict):
            response['chunk_info'] = {
                'chunk_index': int(chunk_index),
                'total_chunks': int(total_chunks),
                'is_chunked': is_chunked == 'true'
            }
        
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            "error": f"Failed to load chunk {chunk_index}: {str(e)}",
            "chunk_info": {
                'chunk_index': int(chunk_index),
                'total_chunks': int(total_chunks),
                'is_chunked': is_chunked == 'true'
            }
        }), 500


@admin_bp.route('/add-user', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data provided"}), 400
    try:
        if user_exists(data):
            return jsonify({"message": "user with this login already exists"}), 400

        user_id, email_sent = create_user(data)
        
        # Provide feedback based on email sending result
        email = data['login']
        if email_sent:
            return jsonify({"message": f"User added successfully! Welcome email sent to {email}"}), 200
        else:
            return jsonify({"message": f"User added successfully, but failed to send welcome email to {email}"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to add user: {str(e)}"}), 500

@admin_bp.route('/cards', methods=['GET'])
@admin_required
def get_all_cards():
    cards = retrieve_all_image_codes_from_cards()
    return jsonify(cards)


@admin_bp.route('/card/<image_code>', methods=['DELETE'])
@admin_required
def delete_card(image_code):
    response, status  = delete_card_by_image_code(image_code)
    return response, status


@admin_bp.route('/card/<image_code>', methods=['GET'])
@admin_required
def get_card(image_code):
    # to get image -> go to image blueprint
    card = find_card_by_image_code(image_code)
    parsed_card = parse_json(card)
    if not parsed_card:
        return jsonify({"error": "No cards available in the database."}), 400

    return jsonify(parsed_card)

@admin_bp.route('/correct', methods=["POST"])
@admin_required
def receive_correct_card():
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

    if update_card(card_id, data):
        increment_correct(card_id, 'admin', EXPECTED_CHECKS_PER_CARD+1)
        return jsonify({"message": "Card marked as correct and updated."}), 200
    else:
        return jsonify({"error": "Error updating card."}), 500


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users"""
    try:
        users = get_all_users()
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get users: {str(e)}"}), 500



@admin_bp.route('/users/<login>/revoke', methods=['POST'])
@admin_required
def revoke_user_endpoint(login):
    """Revoke a user by login"""
    try:
        if revoke_user(login):
            return jsonify({"message": f"User {login} revoked successfully"}), 200
        else:
            return jsonify({"error": f"User {login} not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to revoke user: {str(e)}"}), 500

@admin_bp.route('/users/<login>/unrevoke', methods=['POST'])
@admin_required
def unrevoke_user_endpoint(login):
    """Unrevoke a user by login"""
    try:
        if unrevoke_user(login):
            return jsonify({"message": f"User {login} unrevoked successfully"}), 200
        else:
            return jsonify({"error": f"User {login} not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to unrevoke user: {str(e)}"}), 500
