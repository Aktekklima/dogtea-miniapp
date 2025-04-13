import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models import User, Dog
from app import db
from utils.user_utils import get_or_create_user, update_user_language, get_user_profile
from utils.dog_utils import get_user_dogs, create_new_dog
from utils.language_utils import get_text
from config import DOG_BREEDS, DOG_PRICING, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - introduce the bot and register the user."""
    user = update.effective_user
    language_code = user.language_code if user.language_code in SUPPORTED_LANGUAGES else 'en'
    
    # Get or create user in database
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, language_code)
    
    # Get welcome text in user's language
    welcome_text = get_text('welcome_message', language_code).format(user.first_name)
    
    # Create inline keyboard with Play button
    keyboard = [
        [InlineKeyboardButton(get_text('play_button', language_code), callback_data="play_menu")],
        [InlineKeyboardButton(get_text('my_dogs_button', language_code), callback_data="my_dogs")],
        [InlineKeyboardButton(get_text('shop_button', language_code), callback_data="shop_menu")]
    ]
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command - show available commands and brief explanations."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    help_text = get_text('help_message', language_code)
    
    await update.message.reply_text(help_text)

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /profile command - show user profile with stats."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    profile_data = get_user_profile(db_user.telegram_id)
    profile_text = get_text('profile_message', language_code).format(
        username=profile_data['username'],
        level=profile_data['level'],
        xp=profile_data['xp'],
        next_level_xp=(profile_data['level'] + 1) *
        100,
        dogtea_balance=profile_data['dogtea_balance'],
        dogs_count=profile_data['dogs_count'],
        games_left=profile_data['games_left']
    )
    
    await update.message.reply_text(profile_text)

async def dogs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /dogs command - show user's dogs and their stats."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    dogs = get_user_dogs(db_user.id)
    
    if not dogs:
        no_dogs_text = get_text('no_dogs_message', language_code)
        keyboard = [[InlineKeyboardButton(get_text('shop_button', language_code), callback_data="shop_menu")]]
        
        await update.message.reply_text(
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
    
    await update.message.reply_text(
        dogs_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /shop command - show available dogs for purchase."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
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
    
    await update.message.reply_text(
        shop_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /daily command - claim daily rewards."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Check if the user can play more games today and reset if needed
    can_play = db_user.can_play_game()
    
    daily_text = get_text('daily_message', language_code).format(
        games_left=db_user.games_left_today,
        ad_games_left=max(0, 2 - db_user.ad_games_used)
    )
    
    keyboard = []
    if can_play:
        keyboard.append([
            InlineKeyboardButton(
                get_text('play_button', language_code), 
                callback_data="play_menu"
            )
        ])
    
    if db_user.ad_games_used < 2:
        keyboard.append([
            InlineKeyboardButton(
                get_text('watch_ad_button', language_code), 
                callback_data="watch_ad"
            )
        ])
    
    await update.message.reply_text(
        daily_text,
        reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
    )

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /language command - change user language."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    language_text = get_text('language_selection', language_code)
    
    # Create language selection buttons
    keyboard = [
        [
            InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")
        ]
    ]
    
    await update.message.reply_text(
        language_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def referral_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /referral command - generate referral link."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    bot_username = context.bot.username
    referral_link = f"https://t.me/{bot_username}?start={user.id}"
    
    referral_text = get_text('referral_message', language_code).format(
        referral_link=referral_link
    )
    
    await update.message.reply_text(referral_text)
