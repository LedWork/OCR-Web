from flask import jsonify, request, Blueprint, session
from app.auth.models import user_exists, password_correct

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"message": "OK"}), 200
    return jsonify({"message": "User not logged in"}), 401


@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    if data is None or 'login' not in data or 'password' not in data:
        return jsonify({"message": "Login or password incorrect."}), 400

    if user_exists is False:
        return jsonify({"message": "Login or password incorrect."}), 400

    if password_correct:
        session['user'] = data['login']
        return jsonify({"message": "Sucessfully logged in."}), 200
    else:
        return jsonify({"message": "Login or password incorrect."}), 400
