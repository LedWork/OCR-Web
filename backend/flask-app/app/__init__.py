import os

from flask import Flask, session, render_template, jsonify
from flask_session import Session
from datetime import timedelta
from app.core.db import get_db
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS

app = Flask(__name__, static_folder="dist/static", template_folder="dist", static_url_path="/static")
csrf = CSRFProtect(app)
db = get_db()
CORS(app)

app.config['SESSION_TYPE'] = 'mongodb'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "SECRET")
app.config['SESSION_PERMANENT'] = True  # bo czas ustawiamy
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_MONGODB'] = db.client
app.config['SESSION_MONGODB_DB'] = db.name
app.config['SESSION_MONGODB_COLLECT'] = 'sessions'
app.config.from_object(__name__)
Session(app)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.views import auth_bp
from app.image.views import image_bp
from app.retraining.views import retraining_bp

csrf.exempt(retraining_bp)
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(card_bp, url_prefix="/api/card")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(retraining_bp, url_prefix='/api/retraining')



@app.route("/api/csrf-token", methods=["GET"])
def csrf_token():
    token = generate_csrf()
    return jsonify({"csrf_token": token})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return render_template("index.html")


@app.after_request
def add_csrf_cookie(response):
    if response.status_code in range(200, 400) and not response.direct_passthrough:
        response.set_cookie("csrftoken", generate_csrf(), secure=True)
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)