from flask import session, jsonify
from functools import wraps
from app.auth.model import is_admin

def login_required(f):
    """
    Decorator to restrict access to endpoints for logged-in users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"status": "error", "message": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to restrict access to endpoints for admin users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login = session.get('user')
        if not login or not is_admin(login):
            return jsonify({"status": "error", "message": "Unauthorized. Admin access required."}), 401
        return f(*args, **kwargs)
    return decorated_function
