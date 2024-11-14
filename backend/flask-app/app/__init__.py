from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app.admin.views import admin_bp
from app.card.views import card_bp

app.register_blueprint(admin_bp)
app.register_blueprint(card_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
