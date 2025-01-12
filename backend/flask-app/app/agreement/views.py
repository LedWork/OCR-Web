from flask import Blueprint, request, session, redirect, url_for, abort
from app.core.db import get_db
from bson.objectid import ObjectId
from datetime import datetime
from app.auth.decorators import login_required
from flask import jsonify

agreement_bp = Blueprint("agreement", __name__)


@agreement_bp.route("/", methods=["GET"])
@login_required
def get_contract():
    """
    Handles the GET request for the contract agreement route.
    Checks if the user has already agreed to the contract.
    """
    user_id = session.get("user")
    if not user_id:
        return jsonify({"error": "User ID is missing from session"}), 400

    db = get_db()
    user = db["users"].find_one({"_id": ObjectId(user_id)})

    if user and user.get("agreed_to_contract"):
        return jsonify({"message": "You have already agreed to the contract."}), 200

    return jsonify({"message": "You have not agreed to the contract yet."}), 200


@agreement_bp.route("/", methods=["POST"])
@login_required
def post_contract():
    """
    Handles the POST request for the contract agreement route.
    Updates the user's agreement status if they agree to the contract.
    """
    user_id = session.get("user")
    db = get_db()
    data = request.get_json()  # Expect JSON payload
    agree = data.get("agree")

    if agree == "on":  # User agreed
        db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "agreed_to_contract": True,
                    "contract_accepted_at": datetime.utcnow(),
                }
            },
        )
        return jsonify({"message": "Contract agreement successful."}), 200

    return jsonify({"error": "You must agree to the contract to use the app."}), 403
