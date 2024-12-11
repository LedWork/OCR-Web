from flask import jsonify, request, Blueprint, session

session_bp = Blueprint('sesion', __name__)


@session_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"message": "OK"}), 200
    return jsonify({"message": "User not logged in"}), 401