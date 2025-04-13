import logging
from datetime import date
from app import db
from models import User, Dog, Transaction

logger = logging.getLogger(__name__)

def get_or_create_user(telegram_id, username, first_name, last_name, language_code):
    """Get existing user or create a new one."""
    user = User.query.filter_by(telegram_id=telegram_id).first()
    
    if user:
        # Update user info if needed
        if user.username != username or user.first_name != first_name or user.last_name != last_name:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            db.session.commit()
        
        # Reset daily game limits if needed
        today = date.today()
        
        if user.last_reset_date != today:
            user.games_played_today = 0
            user.games_left_today = 2
            user.ad_games_used = 0
            user.last_reset_date = today
            db.session.commit()
        
        return user
    
    # Create new user
    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
        xp=0,
        level=1,
        dogtea_balance=10,  # Initial balance
        games_played_today=0,
        games_left_today=2,
        last_reset_date=date.today(),
        ad_games_used=0
    )
    
    db.session.add(user)
    
    # Record initial balance transaction
    transaction = Transaction(
        user_id=user.id,
        type="signup_bonus",
        amount=10,
        currency="DOGTEA",
        description="Initial signup bonus"
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    logger.info(f"Created new user: {telegram_id} ({username})")
    return user

def update_user_language(telegram_id, language_code):
    """Update user's preferred language."""
    user = User.query.filter_by(telegram_id=telegram_id).first()
    
    if user:
        user.language_code = language_code
        db.session.commit()
        
        logger.info(f"Updated language for user {telegram_id} to {language_code}")
    
    return user

def get_user_profile(telegram_id):
    """Get user profile information."""
    user = User.query.filter_by(telegram_id=telegram_id).first()
    
    if not user:
        return None
    
    # Count user's dogs
    dogs_count = Dog.query.filter_by(user_id=user.id).count()
    
    return {
        'username': user.username or user.first_name,
        'level': user.level,
        'xp': user.xp,
        'dogtea_balance': user.dogtea_balance,
        'dogs_count': dogs_count,
        'games_played_today': user.games_played_today,
        'games_left_today': user.games_left_today
    }

def update_user_xp(user, xp_amount):
    """Add XP to user and handle level ups."""
    user.xp += xp_amount
    
    # Simple level calculation: level = XP / 100 (rounded down) + 1
    new_level = (user.xp // 100) + 1
    
    level_ups = 0
    if new_level > user.level:
        level_ups = new_level - user.level
        user.level = new_level
    
    db.session.commit()
    
    logger.info(f"Added {xp_amount} XP to user {user.id}, level is now {user.level}")
    return level_ups
