from flask import Flask, session
from flask_session import Session

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'mongodb' 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_PERMANENT'] = True #bo czas ustawiamy 
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config.from_object(__name__)
Session(app)

from app.admin.views import admin_bp
from app.card.views import card_bp
from app.auth.login import login_bp

app.register_blueprint(admin_bp)
app.register_blueprint(card_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
