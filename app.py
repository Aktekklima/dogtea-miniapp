import os
import logging

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Flask app
app = Flask(name)
app.secret_key = os.environ.get("SESSION_SECRET", "dogtea_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///dogtea.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    import models  # noqa: F401
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webapp')
def webapp():
    return render_template('webapp.html')

@app.route('/api/user_info', methods=['POST'])
def user_info():
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
    from models import User, Dog
    data = request.json
    telegram_id = data.get('telegram_id')
    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    dogs = Dog.query.filter_by(user_id=user.id).all()
    dog_list = [{
        'id': dog.id,
        'name': dog.name,
        'breed': dog.breed,
        'level': dog.level,
        'strength': dog.strength,
        'mining_power': dog.mining_power,
        'upgrade_cost': dog.upgrade_cost
    } for dog in dogs]

    return jsonify({'dogs': dog_list})

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)
