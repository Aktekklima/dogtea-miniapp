import datetime
from app import db
from sqlalchemy.sql import func

class User(db.Model):
    """User model for storing Telegram user data"""
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    language_code = db.Column(db.String(10), default='en')
    
    # User stats
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    dogtea_balance = db.Column(db.Float, default=0)
    
    # Gameplay limits
    games_played_today = db.Column(db.Integer, default=0)
    games_left_today = db.Column(db.Integer, default=2)
    last_reset_date = db.Column(db.Date, default=datetime.date.today)
    ad_games_used = db.Column(db.Integer, default=0)
    
    # User preferences
    notification_enabled = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    dogs = db.relationship('Dog', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    battles = db.relationship('Battle', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def can_play_game(self):
        """Check if user can play more games today"""
        today = datetime.date.today()
        
        # Reset daily limits if it's a new day
        if self.last_reset_date != today:
            self.games_played_today = 0
            self.games_left_today = 2
            self.ad_games_used = 0
            self.last_reset_date = today
            db.session.commit()
        
        return self.games_left_today > 0
    
    def add_xp(self, amount):
        """Add XP to user and handle level ups"""
        self.xp += amount
        
        # Simple level calculation: level = XP / 100 (rounded down) + 1
        new_level = (self.xp // 100) + 1
        
        if new_level > self.level:
            # Level up!
            old_level = self.level
            self.level = new_level
            return new_level - old_level  # Return number of levels gained
        
        return 0  # No level up
    
    def add_dogtea(self, amount):
        """Add DOGTEA tokens to user balance"""
        self.dogtea_balance += amount
        db.session.commit()
        return self.dogtea_balance


class Dog(db.Model):
    """Dog model for the mining dogs owned by users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Dog attributes
    name = db.Column(db.String(64), nullable=False)
    breed = db.Column(db.String(64), nullable=False)
    level = db.Column(db.Integer, default=1)
    strength = db.Column(db.Integer, default=10)
    mining_power = db.Column(db.Float, default=1.0)
    
    # Dog economics
    price = db.Column(db.Float, default=5.0)  # Price in TON
    upgrade_cost = db.Column(db.Float, default=1.0)  # Cost in DOGTEA
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<Dog {self.name} ({self.breed})>'
    
    def upgrade(self):
        """Upgrade the dog to the next level"""
        self.level += 1
        self.strength += 5
        self.mining_power += 0.5
        
        # Increase upgrade cost for next level
        self.upgrade_cost *= 1.5
        
        db.session.commit()
        return True


class Transaction(db.Model):
    """Transaction model for tracking DOGTEA and TON transactions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Transaction details
    type = db.Column(db.String(32), nullable=False)  # 'mining', 'game_reward', 'purchase', etc.
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)  # 'DOGTEA' or 'TON'
    description = db.Column(db.String(256))
    
    # For TON transactions
    tx_hash = db.Column(db.String(128))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Transaction {self.type} {self.amount} {self.currency}>'


class Battle(db.Model):
    """Battle model for tracking VS battles between users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opponent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Battle details
    user_dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    opponent_dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Reward
    reward_amount = db.Column(db.Float, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=func.now())
    
    def __repr__(self):
        return f'<Battle {self.id} between {self.user_id} and {self.opponent_id}>'
