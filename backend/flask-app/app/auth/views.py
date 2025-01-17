from flask import jsonify, request, Blueprint, session
from app.auth.model import user_exists, password_correct
from app.auth.model import is_admin

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"message": "OK"}), 200
    return jsonify({"message": "User not logged in"}), 401

@auth_bp.route('/session-admin', methods=['GET'])
def check_admin_session():
    if 'user' not in session:
        return jsonify({"message": "No user logged in."}), 401

    login = session['user']

    if not is_admin(login):
        return jsonify({"status": "error", "message": "Unauthorized. Admin access required. Bla Bla"}), 401
    return jsonify({"status": "success", "message": "Admin access verified."}), 200

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    print(data)
    if data is None or 'login' not in data or 'password' not in data:
        return jsonify({"message": "Login or password incorrect."}), 401

    if user_exists(data['login']) is False:
        return jsonify({"message": "Login or password incorrect."}), 401

    if password_correct(data['login'], data['password']):
        session['user'] = data['login']

        return jsonify({"message": "Sucessfully logged in."}), 200
    else:
        return jsonify({"message": "Login or password incorrect."}), 401

@auth_bp.route('/break-session', methods=['POST'])
def break_session():
    session.clear()
    return jsonify({"message": "Session ended"}), 200