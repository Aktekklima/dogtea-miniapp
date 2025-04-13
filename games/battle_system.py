import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models import User, Dog, Battle
from app import db
from utils.language_utils import get_text
from utils.dog_utils import get_dog_by_id
from utils.token_utils import add_dogtea_reward
from config import GAMES, XP_REWARDS

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE, user, dog_id, language_code, callback=False):
    """Start a battle between the user's dog and a random opponent."""
    # Get the user's dog
    dog = get_dog_by_id(dog_id)
    
    if not dog or dog.owner.telegram_id != user.telegram_id:
        battle_text = get_text('invalid_dog', language_code)
        
        if callback:
            await update.callback_query.edit_message_text(battle_text)
        else:
            await update.message.reply_text(battle_text)
        return
    
    # Find a random opponent (either another user's dog or an NPC dog)
    opponent_dog = find_opponent(dog.user_id, dog.level)
    
    if not opponent_dog:
        # Create NPC dog if no suitable opponent found
        opponent_dog = create_npc_dog(dog.level)
    
    # Set up battle state
    context.user_data['battle'] = {
        'user_dog': dog,
        'opponent_dog': opponent_dog,
        'turn': 0,
        'user_hp': 100,
        'opponent_hp': 100,
        'log': []
    }
    
    # Create battle message
    battle_text = get_text('battle_start', language_code).format(
        dog_name=dog.name,
        dog_breed=dog.breed,
        dog_level=dog.level,
        opponent_name=opponent_dog.name,
        opponent_breed=opponent_dog.breed,
        opponent_level=opponent_dog.level
    )
    
    # Create battle keyboard
    keyboard = [
        [
            InlineKeyboardButton(get_text('attack_button', language_code), callback_data="battle_attack"),
            InlineKeyboardButton(get_text('special_button', language_code), callback_data="battle_special")
        ],
        [
            InlineKeyboardButton(get_text('defend_button', language_code), callback_data="battle_defend")
        ]
    ]
    
    if callback:
        await update.callback_query.edit_message_text(
            battle_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            battle_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def find_opponent(user_id, level):
    """Find a suitable opponent for battle."""
    # Look for dogs with similar level to the user's dog
    min_level = max(1, level - 2)
    max_level = level + 2
    
    # Find another user's dog with similar level
    opponent_dogs = Dog.query.filter(
        Dog.user_id != user_id,
        Dog.level >= min_level,
        Dog.level <= max_level
    ).all()
    
    if opponent_dogs:
        return random.choice(opponent_dogs)
    
    return None

def create_npc_dog(level):
    """Create an NPC dog for battle."""
    from config import DOG_BREEDS
    
    # Create a temporary dog object for battle
    npc_dog = Dog(
        user_id=-1,  # -1 indicates NPC
        name=f"NPC-{random.randint(1000, 9999)}",
        breed=random.choice(DOG_BREEDS),
        level=level,
        strength=10 + (level * 5),
        mining_power=1.0 + (level * 0.5)
    )
    
    return npc_dog

async def handle_battle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle battle action callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    language_code = context.user_data.get('language_code', 'en')
    
    if 'battle' not in context.user_data:
        await query.edit_message_text(get_text('battle_expired', language_code))
        return
    
    battle_data = context.user_data['battle']
    battle_data['turn'] += 1
    
    user_dog = battle_data['user_dog']
    opponent_dog = battle_data['opponent_dog']
    
    # Process user action
    action_result = None
    
    if callback_data == "battle_attack":
        # Regular attack
        damage = calculate_damage(user_dog, "attack")
        battle_data['opponent_hp'] -= damage
        
        action_result = get_text('battle_attack_result', language_code).format(
            dog_name=user_dog.name,
            damage=damage,
            opponent_hp=max(0, battle_data['opponent_hp'])
        )
    
    elif callback_data == "battle_special":
        # Special attack - more damage but can miss
        if random.random() < 0.7:  # 70% success rate
            damage = calculate_damage(user_dog, "special")
            battle_data['opponent_hp'] -= damage
            
            action_result = get_text('battle_special_success', language_code).format(
                dog_name=user_dog.name,
                damage=damage,
                opponent_hp=max(0, battle_data['opponent_hp'])
            )
        else:
            action_result = get_text('battle_special_miss', language_code).format(
                dog_name=user_dog.name
            )
    
    elif callback_data == "battle_defend":
        # Defend - reduce incoming damage and heal a bit
        heal_amount = random.randint(5, 15)
        battle_data['user_hp'] = min(100, battle_data['user_hp'] + heal_amount)
        
        action_result = get_text('battle_defend_result', language_code).format(
            dog_name=user_dog.name,
            heal=heal_amount,
            user_hp=battle_data['user_hp']
        )
    
    battle_data['log'].append(action_result)
    
    # Check if opponent is defeated
    if battle_data['opponent_hp'] <= 0:
        # User wins!
        await handle_battle_end(update, context, True, language_code)
        return
    
    # Opponent's turn
    opponent_action = random.choice(["attack", "special", "defend"])
    opponent_result = None
    
    if opponent_action == "attack":
        damage = calculate_damage(opponent_dog, "attack")
        battle_data['user_hp'] -= damage
        
        opponent_result = get_text('battle_attack_result', language_code).format(
            dog_name=opponent_dog.name,
            damage=damage,
            opponent_hp=max(0, battle_data['user_hp'])
        )
    
    elif opponent_action == "special":
        if random.random() < 0.7:  # 70% success rate
            damage = calculate_damage(opponent_dog, "special")
            battle_data['user_hp'] -= damage
            
            opponent_result = get_text('battle_special_success', language_code).format(
                dog_name=opponent_dog.name,
                damage=damage,
                opponent_hp=max(0, battle_data['user_hp'])
            )
        else:
            opponent_result = get_text('battle_special_miss', language_code).format(
                dog_name=opponent_dog.name
            )
    
    elif opponent_action == "defend":
        heal_amount = random.randint(5, 15)
        battle_data['opponent_hp'] = min(100, battle_data['opponent_hp'] + heal_amount)
        
        opponent_result = get_text('battle_defend_result', language_code).format(
            dog_name=opponent_dog.name,
            heal=heal_amount,
            user_hp=battle_data['opponent_hp']
        )
    
    battle_data['log'].append(opponent_result)
    
    # Check if user is defeated
    if battle_data['user_hp'] <= 0:
        # User loses
        await handle_battle_end(update, context, False, language_code)
        return
    
    # Continue battle
    battle_text = get_text('battle_continue', language_code).format(
        turn=battle_data['turn'],
        user_dog=user_dog.name,
        user_hp=battle_data['user_hp'],
        opponent_dog=opponent_dog.name,
        opponent_hp=battle_data['opponent_hp']
    )
    
    # Add last 2 actions to the message
    if len(battle_data['log']) >= 2:
        last_actions = battle_data['log'][-2:]
        battle_text += "\n\n" + "\n".join(last_actions)
    
    # Create battle keyboard
    keyboard = [
        [
            InlineKeyboardButton(get_text('attack_button', language_code), callback_data="battle_attack"),
            InlineKeyboardButton(get_text('special_button', language_code), callback_data="battle_special")
        ],
        [
            InlineKeyboardButton(get_text('defend_button', language_code), callback_data="battle_defend")
        ]
    ]
    
    await query.edit_message_text(
        battle_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def calculate_damage(dog, attack_type):
    """Calculate damage for battle actions."""
    base_damage = dog.strength // 2
    
    if attack_type == "attack":
        # Regular attack: base damage +/- 20%
        variation = base_damage * random.uniform(-0.2, 0.2)
        return max(1, round(base_damage + variation))
    
    elif attack_type == "special":
        # Special attack: 1.5x base damage +/- 30%
        special_damage = base_damage * 1.5
        variation = special_damage * random.uniform(-0.3, 0.3)
        return max(1, round(special_damage + variation))
    
    return base_damage

async def handle_battle_end(update: Update, context: ContextTypes.DEFAULT_TYPE, is_winner, language_code):
    """Handle the end of a battle."""
    query = update.callback_query
    battle_data = context.user_data['battle']
    
    user_dog = battle_data['user_dog']
    opponent_dog = battle_data['opponent_dog']
    
    # Record battle in database
    from models import User
    user = User.query.filter_by(id=user_dog.user_id).first()
    
    if opponent_dog.user_id != -1:  # Not an NPC
        opponent = User.query.filter_by(id=opponent_dog.user_id).first()
        opponent_id = opponent.id
    else:
        opponent_id = None
    
    # Create battle record
    battle = Battle(
        user_id=user.id,
        opponent_id=opponent_id if opponent_id else user.id,  # Use user's ID as placeholder for NPC
        user_dog_id=user_dog.id,
        opponent_dog_id=opponent_dog.id if opponent_dog.user_id != -1 else None,
        winner_id=user.id if is_winner else (opponent_id if opponent_id else None)
    )
    
    if is_winner:
        # Calculate reward based on dog levels
        base_reward = GAMES['battle']['base_reward']
        level_multiplier = GAMES['battle']['level_multiplier']
        
        reward = base_reward * (level_multiplier ** (opponent_dog.level - 1))
        battle.reward_amount = reward
        
        # Add reward to user
        add_dogtea_reward(user, reward, "battle_win")
        
        # Add XP for winning
        user.add_xp(XP_REWARDS['game_win'])
        
        # Create win message
        result_text = get_text('battle_win', language_code).format(
            dog_name=user_dog.name,
            opponent_name=opponent_dog.name,
            reward=reward
        )
        
        # Add battle log summary
        log_summary = "\n\n" + get_text('battle_log', language_code) + "\n"
        log_summary += "\n".join(battle_data['log'][-4:])  # Last 4 actions
        
        await query.edit_message_text(result_text + log_summary)
    else:
        # User lost
        result_text = get_text('battle_lose', language_code).format(
            dog_name=user_dog.name,
            opponent_name=opponent_dog.name
        )
        
        # Add battle log summary
        log_summary = "\n\n" + get_text('battle_log', language_code) + "\n"
        log_summary += "\n".join(battle_data['log'][-4:])  # Last 4 actions
        
        await query.edit_message_text(result_text + log_summary)
    
    # Save battle record
    db.session.add(battle)
    db.session.commit()
    
    # Clear battle data
    context.user_data.pop('battle', None)
