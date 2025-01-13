from flask import Blueprint, request, session, redirect, url_for, abort
from app.core.db import get_db
from bson.objectid import ObjectId
from datetime import datetime
from app.auth.decorators import login_required
from flask import jsonify

agreement_bp = Blueprint("agreement", __name__)


@agreement_bp.route("/contract", methods=["GET"])
@login_required
def get_contract():
    """
    Handles the GET request for the contract agreement route.
    Checks if the user has already agreed to the contract.
    """
    username = session.get("user")
    print(f"Session username: {username}")  # Log the username

    if not username:
        return jsonify({"error": "Username is missing from session"}), 401

    # Query the database to get the user document by username
    db = get_db()
    collection = db["users"]
    user = collection.find_one({"login": username})
    print(f"User document: {user}")  # Log the user document from the database

    # This is empty

    if not user:
        return jsonify({"error": "User not found"}), 401

    # Get the user_id (ObjectId) from the user document
    user_id = str(user["_id"])  # Convert the ObjectId to string
    print(f"User ID: {user_id}")  # Log the user ID

    # Now, you can safely use the user_id as an ObjectId
    if user.get("agreed_to_contract"):
        print("User has already agreed to the contract.")  # Log agreement status
        return jsonify({"message": "You have already agreed to the contract."}), 200

    print("User has not agreed to the contract yet.")  # Log when the user hasn't agreed
    return jsonify({"message": "You have not agreed to the contract yet."}), 200


@agreement_bp.route("/contract", methods=["POST"])
@login_required
def post_contract():
    """
    Handles the POST request for the contract agreement route.
    Updates the user's agreement status if they agree to the contract.
    """
    # THIS IS USERNAME NOT USER_ID

    user = session.get("user")

    # THIS IS USERNAME NOT USER_ID

    db = get_db()
    collection = db["users"]

    data = request.get_json()  # Expect JSON payload

    if not data:
        return jsonify({"error": "No data provided"}), 407

    agree = data.get("agree")

    if agree == "on":  # User agreed
        collection.update_one(
            {"login": user},
            {
                "$set": {
                    "agreed_to_contract": True,
                    "contract_accepted_at": datetime.utcnow(),
                }
            },
        )
        return jsonify({"message": "Contract agreement successful."}), 200

    return jsonify({"error": "You must agree to the contract to use the app."}), 403
