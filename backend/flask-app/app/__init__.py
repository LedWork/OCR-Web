from flask import Flask, session
from flask_session import Session
from datetime import timedelta
from app.core.db import get_db

import os

app = Flask(__name__)

db = get_db()

app.config['SESSION_TYPE'] = 'mongodb'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = True #bo czas ustawiamy 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_MONGODB'] = db.client
app.config['SESSION_MONGODB_DB'] = db.name
app.config['SESSION_MONGODB_COLLECT'] = 'sessions' 
app.config.from_object(__name__)
Session(app)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.login import login_bp
from app.auth.session import session_bp
from app.image.views import image_bp

app.register_blueprint(admin_bp)
app.register_blueprint(card_bp)
app.register_blueprint(login_bp)
app.register_blueprint(session_bp)
app.register_blueprint(image_bp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
