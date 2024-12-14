from flask import session, jsonify
from functools import wraps


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
