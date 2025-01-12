from flask import Blueprint, request, session, redirect, url_for, abort
from app.core.db import get_db
from bson.objectid import ObjectId
from datetime import datetime
from app.auth.decorators import login_required
from flask import jsonify

agreement_bp = Blueprint("agreement", __name__)


@agreement_bp.route("/agreement", methods=["GET"])
@login_required
def get_contract():
    """
    Handles the GET request for the contract agreement route.
    Renders the contract agreement form if the user hasn't agreed yet.
    """
    user_id = session.get("user")
    db = get_db()
    user = db["users"].find_one({"_id": ObjectId(user_id)})

    # Check if the user has already agreed to the contract
    if user and user.get("agreed_to_contract"):
        # For testing purposes
        # return redirect(url_for("instruction"))
        return jsonify({"message": "You have already agreed to the contract."}), 200

    # Render the contract agreement form


@agreement_bp.route("/agreement", methods=["POST"])
@login_required
def post_contract():
    """
    Handles the POST request for the contract agreement route.
    Updates the user's agreement status if they agree to the contract.
    """
    user_id = session.get("user")
    db = get_db()
    agree = request.form.get("agree")

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

    # If the user submits the form without agreeing
    return jsonify({"error": "You must agree to the contract to use the app."}), 403
