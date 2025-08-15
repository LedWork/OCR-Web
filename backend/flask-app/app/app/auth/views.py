import os
from flask import jsonify, request, Blueprint, session
from app.auth.model import user_exists, password_correct, is_admin, has_password_expired, is_user_revoked
from app.admin.model import generate_user_password
from app.core.db import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/session', methods=['GET'])
def check_session():
    if 'user' in session:
        # Get user email from database
        db = get_db()
        collection = db['users']
        user = collection.find_one({"login": session['user']})
        
        if user and not user.get('is_revoked', False):
            return jsonify({
                "message": "OK",
                "email": user['login']  # login is the email address
            }), 200
        else:
            return jsonify({"message": "Użytkownik nie został znaleziony lub konto zostało odwołane"}), 401
    return jsonify({"message": "Użytkownik nie jest zalogowany"}), 401

@auth_bp.route('/session-admin', methods=['GET'])
def check_admin_session():
    if 'user' not in session:
        return jsonify({"message": "Brak zalogowanego użytkownika."}), 401

    login = session['user']

    if not is_admin(login):
        return jsonify({"status": "error", "message": "Brak autoryzacji. Wymagany dostęp administratora."}), 401
        # Should't there be some kind of return in the place where, we check if the user is admin or not?]
        # This throws an error, that doesn't affect the functionality but it looks bad.
    return jsonify({"status": "success", "message": "Dostęp administratora potwierdzony."}), 200

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    print(data)
    if data is None or 'login' not in data or 'password' not in data:
        return jsonify({"message": "Login lub hasło nieprawidłowe."}), 401

    if user_exists(data['login']) is False:
        return jsonify({"message": "Login lub hasło nieprawidłowe."}), 401

    # Check if user is revoked
    if is_user_revoked(data['login']):
        return jsonify({"message": "Konto zostało odwołane. Skontaktuj się z administratorem."}), 401

    if password_correct(data['login'], data['password']):
        session['user'] = data['login']
        if has_password_expired(data['login']):
            web_server_url = os.getenv('WEB_SERVER_URL', 'https://ocr-pck.eu')
            return jsonify({"message": f"Hasło wygasło, wprowadź email na stronie {web_server_url} aby otrzymać nowe"}), 401

        return jsonify({"message": "Pomyślnie zalogowano."}), 200
    else:
        return jsonify({"message": "Login lub hasło nieprawidłowe."}), 401

@auth_bp.route('/break-session', methods=['POST'])
def break_session():
    session.clear()
    return jsonify({"message": "Sesja zakończona"}), 200

@auth_bp.route('/send-password', methods=['POST'])
def send_password():
    data = request.get_json()

    if data is None or 'login' not in data:
        return jsonify({"message": "Email incorrect."}), 401

    if user_exists(data['login']) is False:
        return jsonify({"message": "User not registered."}), 401

    if generate_user_password(data['login']):
        return jsonify({"message": "Password sent on provided email."}), 200
    else:
        return jsonify({"message": "There was a problem with sending password."}), 401

