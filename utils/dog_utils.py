import logging
import random
from app import db
from models import User, Dog, Transaction
from config import DOG_PRICING

logger = logging.getLogger(__name__)

def get_user_dogs(user_id):
    """Get all dogs owned by a user."""
    return Dog.query.filter_by(user_id=user_id).all()

def get_dog_by_id(dog_id):
    """Get a dog by ID."""
    return Dog.query.get(dog_id)

def create_new_dog(user_id, name, breed):
    """Create a new dog for a user."""
    # Set default price based on breed
    price = DOG_PRICING.get(breed, 5.0)
    
    # Create dog with default attributes
    dog = Dog(
        user_id=user_id,
        name=name,
        breed=breed,
        level=1,
        strength=10,
        mining_power=1.0,
        price=price,
        upgrade_cost=1.0
    )
    
    db.session.add(dog)
    db.session.commit()
    
    logger.info(f"Created new dog: {name} ({breed}) for user {user_id}")
    return dog

def upgrade_dog(dog_id, user):
    """Upgrade a dog to the next level."""
    dog = get_dog_by_id(dog_id)
    
    if not dog:
        logger.error(f"Dog not found: {dog_id}")
        return False
    
    if dog.user_id != user.id:
        logger.error(f"Dog {dog_id} does not belong to user {user.id}")
        return False
    
    # Check if user has enough DOGTEA
    if user.dogtea_balance < dog.upgrade_cost:
        logger.error(f"User {user.id} has insufficient funds for upgrade")
        return False
    
    # Deduct upgrade cost
    user.dogtea_balance -= dog.upgrade_cost
    
    # Record transaction
    transaction = Transaction(
        user_id=user.id,
        type="dog_upgrade",
        amount=dog.upgrade_cost,
        currency="DOGTEA",
        description=f"Upgrade dog {dog.name} from level {dog.level} to {dog.level + 1}"
    )
    db.session.add(transaction)
    
    # Upgrade dog
    old_level = dog.level
    dog.level += 1
    dog.strength += 5 + random.randint(0, 3)  # Add some randomness to strength increase
    dog.mining_power += 0.5
    
    # Increase upgrade cost for next level
    dog.upgrade_cost *= 1.5
    
    db.session.commit()
    
    logger.info(f"Upgraded dog {dog.name} from level {old_level} to {dog.level}")
    return True

def calculate_mining_power(dog):
    """Calculate dog's mining power based on level and breed."""
    base_power = dog.mining_power
    
    # Apply modifiers based on breed if desired
    breed_modifier = 1.0
    if dog.breed == "Golden Retriever":
        breed_modifier = 1.05
    elif dog.breed == "Siberian Husky":
        breed_modifier = 1.1
    elif dog.breed == "Pug":
        breed_modifier = 1.15
    elif dog.breed == "Chihuahua":
        breed_modifier = 1.2
    
    return base_power * breed_modifier
