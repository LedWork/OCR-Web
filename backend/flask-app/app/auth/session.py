from flask import jsonify, request, Blueprint, session

session_bp = Blueprint('sesion', __name__)


@session_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user' in session:
        return {"OK"}, 200
    return {"Error"}, 404