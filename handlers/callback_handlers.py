import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models import User, Dog
from app import db
from utils.user_utils import get_or_create_user, update_user_language
from utils.dog_utils import upgrade_dog, get_dog_by_id
from utils.language_utils import get_text
from games.guess_game import start_guess_game_session
from games.click_game import start_click_game_session
from games.loot_box import open_loot_box
from games.quiz_game import start_quiz_game_session
from games.battle_system import start_battle

logger = logging.getLogger(__name__)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    callback_data = query.data
    
    # Handle play menu
    if callback_data == "play_menu":
        # Same as /play command
        await play_menu(update, context, db_user, language_code)
    
    # Handle my dogs menu
    elif callback_data == "my_dogs":
        # Similar to /dogs command
        await dogs_menu(update, context, db_user, language_code)
    
    # Handle shop menu
    elif callback_data == "shop_menu":
        # Similar to /shop command
        await shop_menu(update, context, db_user, language_code)
    
    # Handle game selection
    elif callback_data.startswith("play_"):
        game_type = callback_data.split("_")[1]
        
        # Check if the user can play more games today
        can_play = db_user.can_play_game()
        
        if not can_play:
            await query.edit_message_text(get_text('no_games_left', language_code))
            return
        
        # Reduce available games and track play
        db_user.games_left_today -= 1
        db_user.games_played_today += 1
        db.session.commit()
        
        # Start selected game
        if game_type == "guess":
            await start_guess_game_session(update, context, language_code, callback=True)
        elif game_type == "click":
            await start_click_game_session(update, context, language_code, callback=True)
        elif game_type == "loot":
            await open_loot_box(update, context, language_code, callback=True)
        elif game_type == "quiz":
            await start_quiz_game_session(update, context, language_code, callback=True)
    
    # Handle dog upgrade
    elif callback_data.startswith("upgrade_dog_"):
        dog_id = int(callback_data.split("_")[2])
        
        # Get the dog and attempt to upgrade
        dog = get_dog_by_id(dog_id)
        
        if not dog or dog.owner.telegram_id != user.id:
            await query.edit_message_text(get_text('invalid_dog', language_code))
            return
        
        # Check if user has enough DOGTEA for upgrade
        if db_user.dogtea_balance < dog.upgrade_cost:
            await query.edit_message_text(
                get_text('insufficient_funds', language_code).format(
                    required=dog.upgrade_cost,
                    balance=db_user.dogtea_balance
                )
            )
            return
        
        # Perform upgrade
        success = upgrade_dog(dog_id, db_user)
        
        if success:
            await query.edit_message_text(
                get_text('dog_upgraded', language_code).format(
                    name=dog.name,
                    level=dog.level,
                    strength=dog.strength,
                    mining_power=dog.mining_power,
                    balance=db_user.dogtea_balance
                )
            )
        else:
            await query.edit_message_text(get_text('upgrade_failed', language_code))
    
    # Handle battle initiation
    elif callback_data.startswith("battle_dog_"):
        dog_id = int(callback_data.split("_")[2])
        
        # Start battle system
        await start_battle(update, context, db_user, dog_id, language_code, callback=True)
    
    # Handle watch ad for more games
    elif callback_data == "watch_ad":
        # Simulate ad watching (in real implementation, integrate ad provider)
        if db_user.ad_games_used < 2:
            db_user.ad_games_used += 1
            db_user.games_left_today += 1
            db.session.commit()
            
            await query.edit_message_text(
                get_text('ad_watched', language_code).format(
                    games_left=db_user.games_left_today
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        get_text('play_button', language_code), 
                        callback_data="play_menu"
                    )]
                ])
            )
        else:
            await query.edit_message_text(get_text('no_more_ads', language_code))

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    
    if callback_data.startswith("lang_"):
        language_code = callback_data.split("_")[1]
        
        # Update user language
        db_user = update_user_language(user.id, language_code)
        
        # Confirm language change
        await query.edit_message_text(get_text('language_changed', language_code))

async def play_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user, language_code):
    """Show play menu with available games."""
    query = update.callback_query
    
    # Check if the user can play more games today
    can_play = db_user.can_play_game()
    
    if not can_play:
        no_games_text = get_text('no_games_left', language_code)
        keyboard = [[
            InlineKeyboardButton(
                get_text('watch_ad_button', language_code), 
                callback_data="watch_ad"
            )
        ]]
        
        await query.edit_message_text(
            no_games_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Show available games
    games_text = get_text('available_games', language_code).format(
        games_left=db_user.games_left_today
    )
    
    keyboard = [
        [
            InlineKeyboardButton(
                get_text('guess_game_button', language_code), 
                callback_data="play_guess"
            ),
            InlineKeyboardButton(
                get_text('click_game_button', language_code), 
                callback_data="play_click"
            )
        ],
        [
            InlineKeyboardButton(
                get_text('loot_box_button', language_code), 
                callback_data="play_loot"
            ),
            InlineKeyboardButton(
                get_text('quiz_game_button', language_code), 
                callback_data="play_quiz"
            )
        ],
        [
            InlineKeyboardButton(
                get_text('back_button', language_code),
                callback_data="back_to_main"
            )
        ]
    ]
    
    await query.edit_message_text(
        games_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def dogs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user, language_code):
    """Show user's dogs and their stats."""
    query = update.callback_query
    
    dogs = Dog.query.filter_by(user_id=db_user.id).all()
    
    if not dogs:
        no_dogs_text = get_text('no_dogs_message', language_code)
        keyboard = [[InlineKeyboardButton(get_text('shop_button', language_code), callback_data="shop_menu")]]
        
        await query.edit_message_text(
            no_dogs_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    dogs_text = get_text('dogs_list_header', language_code)
    
    for i, dog in enumerate(dogs, 1):
        dogs_text += f"\n\n🐕 {i}. {dog.name} ({dog.breed})\n"
        dogs_text += get_text('dog_stats', language_code).format(
            level=dog.level,
            strength=dog.strength,
            mining_power=dog.mining_power,
            upgrade_cost=dog.upgrade_cost
        )
    
    # Add buttons for each dog
    keyboard = []
    for dog in dogs:
        keyboard.append([
            InlineKeyboardButton(
                f"🔄 {get_text('upgrade_button', language_code)} {dog.name}", 
                callback_data=f"upgrade_dog_{dog.id}"
            ),
            InlineKeyboardButton(
                f"⚔️ {get_text('battle_button', language_code)}", 
                callback_data=f"battle_dog_{dog.id}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            get_text('back_button', language_code),
            callback_data="back_to_main"
        )
    ])
    
    await query.edit_message_text(
        dogs_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def shop_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, db_user, language_code):
    """Show shop with available dogs for purchase."""
    query = update.callback_query
    
    from config import DOG_BREEDS, DOG_PRICING
    
    shop_text = get_text('shop_header', language_code)
    
    keyboard = []
    for breed in DOG_BREEDS:
        price = DOG_PRICING.get(breed, 5)
        shop_text += f"\n\n🐕 {breed}\n"
        shop_text += get_text('dog_price', language_code).format(price=price)
        
        keyboard.append([
            InlineKeyboardButton(
                f"{breed} - {price} TON", 
                callback_data=f"buy_dog_{breed}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            get_text('back_button', language_code),
            callback_data="back_to_main"
        )
    ])
    
    await query.edit_message_text(
        shop_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
