from flask import Flask

app = Flask(__name__)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.login import login_bp

app.register_blueprint(admin_bp)
app.register_blueprint(card_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
