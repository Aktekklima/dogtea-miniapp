import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dogtea_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///dogtea.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()

# Routes for web app
from flask import render_template, jsonify, request, session

@app.route('/')
def index():
    """Main route for the web interface"""
    return render_template('index.html')

@app.route('/webapp')
def webapp():
    """Telegram MiniApp/WebApp route"""
    return render_template('webapp.html')

@app.route('/api/user_info', methods=['POST'])
def user_info():
    """API endpoint to get user information"""
    from models import User
    data = request.json
    telegram_id = data.get('telegram_id')
    
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'username': user.username,
        'xp': user.xp,
        'level': user.level,
        'dogtea_balance': user.dogtea_balance,
        'games_played_today': user.games_played_today,
        'games_left_today': user.games_left_today
    })

@app.route('/api/dog_info', methods=['POST'])
def dog_info():
    """API endpoint to get dog information"""
    from models import User, Dog
    data = request.json
    telegram_id = data.get('telegram_id')
    
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    dogs = Dog.query.filter_by(user_id=user.id).all()
    dog_list = []
    
    for dog in dogs:
        dog_list.append({
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed,
            'level': dog.level,
            'strength': dog.strength,
            'mining_power': dog.mining_power,
            'upgrade_cost': dog.upgrade_cost
        })
    
    return jsonify({'dogs': dog_list})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
