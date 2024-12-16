import os

from flask import Flask, session
from flask_session import Session
from datetime import timedelta
from app.core.db import get_db

app = Flask(__name__)
db = get_db()

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

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(card_bp, url_prefix="/card")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(image_bp, url_prefix='/image')


def get_routes():
    routes = []
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            routes.append({
                "url": rule.rule,
                "methods": list(rule.methods)
            })
    return routes


@app.route('/')
def home():
    return get_routes() # aby moc zobaczyc route'y


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
