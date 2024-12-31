from flask import Blueprint, request, session, redirect, url_for, abort
from app.core.db import get_db
from bson.objectid import ObjectId
from datetime import datetime
from app.auth.decorators import login_required
from flask import jsonify

agreement_bp = Blueprint("contract", __name__, url_prefix="/contract")

@agreement_bp.route("/", methods=["GET"])
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
        return jsonify({"message": "You have already agreed to the contract."}), 200

    # Render the contract agreement form
    return f"""
        <h1>Contract Agreement</h1>
        <pre style="white-space: pre-wrap;">
        # Umowa o Zachowaniu Poufności w Procesie Ręcznej Weryfikacji Zdigitalizowanych Honorowych Kart Krwiodawców

        ## Sekcja 1: Identyfikacja Stron
        - **Administrator Danych**: Polski Czerwony Krzyż z siedzibą w Warszawie (00-561) przy ul. Mokotowskiej 14, iod@pck.pl
        - **Weryfikator**: [Imię i nazwisko, adres, dane kontaktowe]  

        ---

        ## Sekcja 2: Zakres i Cel
        Weryfikator przyjmuje do wiadomości, że:
        1. Jego zadaniem jest wyłącznie potwierdzenie zgodności zdigitalizowanych danych (numery PESEL, imiona i nazwiska, daty urodzenia, ilość oddanej krwi) z zeskanowanymi honorowymi kartami krwiodawców dostarczonymi przez Administratora Danych.
        2. Weryfikator nie nabywa żadnych praw do przechowywania, kopiowania lub wykorzystywania tych danych w celach innych niż wskazane powyżej.

        ---

        ## Sekcja 3: Obowiązki
        Weryfikator zobowiązuje się do:
        1. Wykorzystywania udostępnionych danych osobowych wyłącznie w procesie weryfikacji zgodnie z instrukcjami Administratora Danych.
        2. Zachowania danych w ścisłej poufności i nieujawniania ich osobom trzecim.
        3. Nie kopiowania, zapisywania ani przechowywania danych w żadnej formie poza zatwierdzonym procesem weryfikacji.
        4. Zwrócenia lub usunięcia wszystkich danych po zakończeniu weryfikacji, zgodnie z instrukcjami Administratora Danych.

        ---

        ## Sekcja 4: Zasady RODO
        Weryfikator przyjmuje do wiadomości zasady RODO, w tym:
        1. Przetwarzanie danych zgodnie z prawem, w sposób rzetelny i przejrzysty (**Art. 5 RODO**).
        2. Utrzymanie poufności i integralności danych osobowych (**Art. 32 RODO**).

        ---

        ## Sekcja 5: Konsekwencje Naruszenia
        Naruszenie warunków niniejszej umowy może skutkować:
        1. Natychmiastowym zakończeniem współpracy w ramach procesu weryfikacji.
        2. Podjęciem działań prawnych na podstawie obowiązujących przepisów dotyczących ochrony danych osobowych, w tym kar wynikających z RODO.

        ---

        ## Sekcja 6: Potwierdzenie
        Podpisując tę umowę, Weryfikator potwierdza zrozumienie i akceptację opisanych powyżej obowiązków i zobowiązań.
        </pre>
        <form method="POST">
            <input type="checkbox" name="agree" id="agree">
            <label for="agree">I agree to the terms of this contract</label>
            <br><br>
            <button type="submit">Submit</button>
        </form>
    """

@agreement_bp.route("/", methods=["POST"])
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
