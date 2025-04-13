import os
import logging
import telebot
import json
from config import TELEGRAM_BOT_TOKEN, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_bot():
    """Initialize and start the bot"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    if not token:
        logger.error("Telegram bot token not found!")
        return
    
    logger.info("Starting bot...")
    
    # Create bot instance
    bot = telebot.TeleBot(token)
    
    # Import models and utils
    from app import db
    from models import User, Dog, Transaction
    from utils.user_utils import get_or_create_user
    from utils.dog_utils import get_user_dogs, create_new_dog
    
    # Load language files
    languages = {}
    for lang_code in SUPPORTED_LANGUAGES:
        try:
            module = __import__(f"locales.{lang_code}", fromlist=['texts'])
            languages[lang_code] = module.texts
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load language {lang_code}: {e}")
            # Fallback to English if a language file fails to load
            if lang_code != DEFAULT_LANGUAGE:
                module = __import__(f"locales.{DEFAULT_LANGUAGE}", fromlist=['texts'])
                languages[lang_code] = module.texts
    
    def get_text(key, lang_code=DEFAULT_LANGUAGE):
        """Get text in the specified language."""
        if lang_code not in languages:
            lang_code = DEFAULT_LANGUAGE
        return languages[lang_code].get(key, languages[DEFAULT_LANGUAGE].get(key, key))
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        """Handle the /start command - introduce the bot and register the user."""
        logger.info(f"Start command from {message.from_user.username}")
        
        # Get or create user
        user = get_or_create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.language_code
        )
        
        lang_code = user.language_code
        
        # Welcome message
        welcome_msg = get_text('welcome', lang_code).format(name=user.first_name)
        
        # Create keyboard with main options
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        play_button = telebot.types.InlineKeyboardButton(
            get_text('play_button', lang_code),
            callback_data='play_menu'
        )
        
        dogs_button = telebot.types.InlineKeyboardButton(
            get_text('dogs_button', lang_code),
            callback_data='dogs_menu'
        )
        
        shop_button = telebot.types.InlineKeyboardButton(
            get_text('shop_button', lang_code),
            callback_data='shop_menu'
        )
        
        lang_button = telebot.types.InlineKeyboardButton(
            get_text('language_button', lang_code),
            callback_data='change_language'
        )
        
        webapp_button = telebot.types.InlineKeyboardButton(
            get_text('webapp_button', lang_code),
            web_app={"url": "http://0.0.0.0:5000/webapp"}
        )
        
        markup.add(play_button, dogs_button)
        markup.add(shop_button, lang_button)
        markup.add(webapp_button)
        
        bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)
    
    @bot.message_handler(commands=['help'])
    def help_command(message):
        """Handle the /help command - show available commands."""
        # Get user language
        user = User.query.filter_by(telegram_id=message.from_user.id).first()
        lang_code = user.language_code if user else message.from_user.language_code
        
        help_text = get_text('help_text', lang_code)
        bot.send_message(message.chat.id, help_text)
    
    @bot.message_handler(commands=['profile'])
    def profile_command(message):
        """Handle the /profile command - show user profile."""
        # Get user
        user = User.query.filter_by(telegram_id=message.from_user.id).first()
        if not user:
            bot.send_message(message.chat.id, "Please use /start first to create your profile.")
            return
        
        lang_code = user.language_code
        
        # Get user dogs
        dogs = get_user_dogs(user.id)
        dog_count = len(dogs)
        
        profile_text = get_text('profile_text', lang_code).format(
            username=user.username or message.from_user.first_name,
            level=user.level,
            xp=user.xp,
            xp_next=(user.level + 1) * 100,
            dogtea=user.dogtea_balance,
            dogs=dog_count,
            games_left=user.games_left_today
        )
        
        bot.send_message(message.chat.id, profile_text)
    
    @bot.message_handler(commands=['webapp'])
    def webapp_command(message):
        """Send a message with a WebApp button."""
        # Get user language
        user = User.query.filter_by(telegram_id=message.from_user.id).first()
        lang_code = user.language_code if user else message.from_user.language_code
        
        markup = telebot.types.InlineKeyboardMarkup()
        webapp_button = telebot.types.InlineKeyboardButton(
            get_text('open_webapp', lang_code),
            web_app={"url": "http://0.0.0.0:5000/webapp"}
        )
        markup.add(webapp_button)
        
        bot.send_message(
            message.chat.id,
            get_text('webapp_text', lang_code),
            reply_markup=markup
        )
    
    # Start the bot
    logger.info("Bot polling started")
    bot.polling(none_stop=True)
    
    logger.info("Bot stopped")

if __name__ == "__main__":
    start_bot()
