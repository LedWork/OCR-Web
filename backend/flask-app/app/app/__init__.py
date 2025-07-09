import os
import logging

from flask import Flask, session, render_template, jsonify
from flask_session import Session
from datetime import timedelta
from app.core.db import get_db, ensure_admin_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
from flask_talisman import Talisman
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder="dist/static", # vol/static for production
    template_folder="dist",
    static_url_path="/static",
)
db = get_db()
ensure_admin_user(db)
app.config["SESSION_TYPE"] = "mongodb"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET")
app.config["SESSION_PERMANENT"] = True  # bo czas ustawiamy
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.config["SESSION_MONGODB"] = db.client
app.config["SESSION_MONGODB_DB"] = db.name
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
app.config.from_object(__name__)
Session(app)

csrf = CSRFProtect(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:80"}})
talisman = Talisman(
    app,
    force_https=False,
    x_content_type_options='nosniff',
    content_security_policy={ # change to https later
        'default-src': ["'self'", 'strict-dynamic'],
        'script-src': ["'self'", 'http://localhost:80'],
        'style-src': ["'self'", 'http://localhost:80'],
        'img-src': ["'self'", 'data:', 'http://localhost:80'],
        'connect-src': ["'self'", 'http://localhost:80'],
        'frame-ancestors': ["'none'"],
        'form-action': ["'self'", 'http://localhost:80'],
    },
    strict_transport_security=True,
    frame_options='DENY',
    x_xss_protection='1; mode=block',
    referrer_policy='strict-origin-when-cross-origin'
)

# Email configuration with validation and logging
mail_server = os.getenv("MAIL_SERVER")
mail_port = os.getenv('MAIL_PORT')
mail_username = os.getenv("MAIL_USERNAME")
mail_password = os.getenv("MAIL_PASSWORD")

# Log email configuration (without password for security)
logger.info(f"Email configuration - Server: {mail_server}, Port: {mail_port}, Username: {mail_username}")

# Validate email configuration
if not all([mail_server, mail_port, mail_username, mail_password]):
    logger.error("Missing email configuration variables. Please check MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD")
    logger.error(f"Current values - Server: {mail_server}, Port: {mail_port}, Username: {mail_username}, Password: {'SET' if mail_password else 'NOT SET'}")

app.config['MAIL_SERVER'] = mail_server
app.config['MAIL_PORT'] = int(mail_port) if mail_port else 587
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config['MAIL_DEFAULT_SENDER'] = mail_username
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.views import auth_bp
from app.image.views import image_bp
from app.agreement.views import agreement_bp
from app.retraining.views import retraining_bp

csrf.exempt(retraining_bp)
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(card_bp, url_prefix="/api/card")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(image_bp, url_prefix="/api/image")
app.register_blueprint(retraining_bp, url_prefix="/api/retraining")
app.register_blueprint(agreement_bp, url_prefix="/api/agreement")

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
        response.set_cookie("csrftoken", generate_csrf(), secure=True, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
