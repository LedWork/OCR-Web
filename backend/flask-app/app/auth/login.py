import bcrypt
from flask import jsonify, request, Blueprint, session

from app.core.db import get_db

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    if data is None or 'login' not in data or 'password' not in data:
        return jsonify({"error": "Login or password incorrect."}), 400

    db = get_db()
    collection = db['users']
    user = collection.find_one({"login": data['login']})

    if user is None:
        return jsonify({"error": "Login or password incorrect."}), 400
    if bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        session['user'] = data['user']
        return jsonify({"Success": "Sucessfully logged in."}), 200
    else:
        return jsonify({"error": "Login or password incorrect."}), 400
