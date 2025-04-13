import logging
from app import db
from models import User, Transaction

logger = logging.getLogger(__name__)

def add_dogtea_reward(user, amount, reward_type):
    """Add DOGTEA tokens to user balance and record transaction."""
    # Add tokens to user balance
    user.dogtea_balance += amount
    
    # Record transaction
    transaction = Transaction(
        user_id=user.id,
        type=reward_type,
        amount=amount,
        currency="DOGTEA",
        description=f"{reward_type.replace('_', ' ').title()} reward"
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    logger.info(f"Added {amount} DOGTEA to user {user.id} for {reward_type}")
    return user.dogtea_balance

def calculate_daily_mining(user):
    """Calculate daily mining rewards based on user's dogs."""
    from models import Dog
    from utils.dog_utils import calculate_mining_power
    from config import MINING_RATE
    
    dogs = Dog.query.filter_by(user_id=user.id).all()
    
    if not dogs:
        return 0
    
    total_mining = 0
    
    for dog in dogs:
        # Get base mining rate for dog's level
        base_rate = MINING_RATE.get(dog.level, 0.5)
        
        # Apply dog's mining power
        mining_power = calculate_mining_power(dog)
        
        # Calculate mining reward
        dog_mining = base_rate * mining_power
        total_mining += dog_mining
    
    return round(total_mining, 1)

def process_daily_mining(user):
    """Process daily mining rewards for a user."""
    # Calculate mining reward
    mining_reward = calculate_daily_mining(user)
    
    if mining_reward <= 0:
        return 0
    
    # Add rewards to user
    add_dogtea_reward(user, mining_reward, "daily_mining")
    
    logger.info(f"Processed daily mining of {mining_reward} DOGTEA for user {user.id}")
    return mining_reward

def get_token_price():
    """Get current DOGTEA token price in TON."""
    # In a real implementation, this would fetch from an API or market
    # For now, return a fixed value
    return 0.01  # 1 DOGTEA = 0.01 TON
