#!/usr/bin/env python
import os
import telebot
import logging
import json
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
API_BASE_URL = "http://localhost:5000/api"

def get_or_create_user(telegram_id, username, first_name, last_name, language_code):
    """Use the Flask API to create or get a user"""
    logger.info(f"Getting or creating user for {telegram_id}")
    
    try:
        # This would be an API call to your Flask app
        # For now, just return a mock user
        return {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language_code": language_code,
            "level": 1,
            "xp": 0,
            "dogtea_balance": 10.0,
            "games_left_today": 2
        }
    except Exception as e:
        logger.error(f"Error getting/creating user: {e}")
        return None

def get_text(key, language_code='en'):
    """Get text in the specified language."""
    # This is a simplified version - in the real app we'd import from locales
    texts = {
        'en': {
            'welcome': 'Welcome to DogTea Mining Bot, {name}! 🐕\n\nStart mining DOGTEA tokens with your virtual dogs. Buy, upgrade, and battle with your dogs to earn more tokens!\n\nUse the menu below to get started:',
            'help_text': '🐕 *DogTea Mining Bot Commands* 🐕\n\n/start - Start the bot and see main menu\n/profile - View your profile and stats\n/dogs - View your dogs and their stats\n/shop - Buy new dogs with TON\n/daily - Check your daily game limits\n/play - Play mini-games to earn DOGTEA\n/language - Change language\n/referral - Get your referral link\n/webapp - Open the DogTea WebApp',
            'profile_text': '👤 *Your Profile*\n\nUsername: {username}\nLevel: {level}\nXP: {xp}/{xp_next}\nDOGTEA Balance: {dogtea}\nDogs: {dogs}\nGames left today: {games_left}',
            'webapp_text': 'Open the DogTea Mining WebApp:',
            'open_webapp': '🎮 Open WebApp',
            'no_dogs_message': 'You don\'t have any dogs yet! Visit the shop to buy your first dog.',
            'admin_message': '⚠️ This is an admin-only command.'
        },
        'tr': {
            'welcome': 'DogTea Mining Bot\'a Hoşgeldin, {name}! 🐕\n\nSanal köpeklerinle DOGTEA token madenciliği yap. Köpekleri satın al, geliştir ve savaştırarak daha fazla token kazan!\n\nBaşlamak için aşağıdaki menüyü kullan:',
            'help_text': '🐕 *DogTea Mining Bot Komutları* 🐕\n\n/start - Botu başlat ve ana menüyü gör\n/profile - Profilini ve istatistiklerini görüntüle\n/dogs - Köpeklerini ve istatistiklerini görüntüle\n/shop - TON ile yeni köpekler satın al\n/daily - Günlük oyun limitlerini kontrol et\n/play - DOGTEA kazanmak için mini oyunlar oyna\n/language - Dil değiştir\n/referral - Referans bağlantını al\n/webapp - DogTea WebApp\'i aç',
            'profile_text': '👤 *Profil Bilgilerin*\n\nKullanıcı Adı: {username}\nSeviye: {level}\nXP: {xp}/{xp_next}\nDOGTEA Bakiye: {dogtea}\nKöpekler: {dogs}\nBugün kalan oyunlar: {games_left}',
            'webapp_text': 'DogTea Mining WebApp\'i aç:',
            'open_webapp': '🎮 WebApp\'i Aç',
            'no_dogs_message': 'Henüz hiç köpeğin yok! İlk köpeğini satın almak için mağazayı ziyaret et.',
            'admin_message': '⚠️ Bu komut yalnızca yöneticiler içindir.'
        }
    }
    
    # Default to English if language not supported
    if language_code not in texts:
        language_code = 'en'
    
    # Return the requested text or key if not found
    return texts[language_code].get(key, texts['en'].get(key, key))

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        exit(1)
    
    logger.info(f"Starting bot with token: {TELEGRAM_BOT_TOKEN[:5]}...")
    
    # Create the bot
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    
    # Define a /start handler
    @bot.message_handler(commands=['start'])
    def start_command(message):
        logger.info(f"Received /start command from {message.from_user.username}")
        
        # Get or create user
        user = get_or_create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.language_code
        )
        
        if not user:
            bot.reply_to(message, "Error creating user. Please try again later.")
            return
        
        lang_code = user.get('language_code', 'en')
        
        # Welcome message
        welcome_msg = get_text('welcome', lang_code).format(name=user.get('first_name', 'User'))
        
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
    
    # Define a /help handler
    @bot.message_handler(commands=['help'])
    def help_command(message):
        logger.info(f"Received /help command from {message.from_user.username}")
        
        # Get user language
        lang_code = message.from_user.language_code or 'en'
        
        help_text = get_text('help_text', lang_code)
        bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
    
    # Define a /profile handler
    @bot.message_handler(commands=['profile'])
    def profile_command(message):
        logger.info(f"Received /profile command from {message.from_user.username}")
        
        # Get user info from API
        user = get_or_create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.language_code
        )
        
        if not user:
            bot.reply_to(message, "Error retrieving user profile. Please try again later.")
            return
        
        lang_code = user.get('language_code', 'en')
        
        # Format profile message
        profile_text = get_text('profile_text', lang_code).format(
            username=user.get('username') or message.from_user.first_name,
            level=user.get('level', 1),
            xp=user.get('xp', 0),
            xp_next=(user.get('level', 1) + 1) * 100,
            dogtea=user.get('dogtea_balance', 0),
            dogs=len(user.get('dogs', [])),
            games_left=user.get('games_left_today', 0)
        )
        
        bot.send_message(message.chat.id, profile_text, parse_mode="Markdown")
    
    # Define a /webapp handler
    @bot.message_handler(commands=['webapp'])
    def webapp_command(message):
        logger.info(f"Received /webapp command from {message.from_user.username}")
        
        # Get user language
        lang_code = message.from_user.language_code or 'en'
        
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
    
    # Define a callback query handler
    @bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        logger.info(f"Received callback query: {call.data} from {call.from_user.username}")
        
        # Get user info from API
        user = get_or_create_user(
            call.from_user.id,
            call.from_user.username,
            call.from_user.first_name,
            call.from_user.last_name,
            call.from_user.language_code
        )
        
        if not user:
            bot.answer_callback_query(call.id, "Error processing request. Please try again later.")
            return
        
        lang_code = user.get('language_code', 'en')
        
        # Handle different callback queries
        if call.data == 'play_menu':
            bot.answer_callback_query(call.id, "Play menu coming soon!")
            # Here you would implement your play menu
            
        elif call.data == 'dogs_menu':
            bot.answer_callback_query(call.id, "Dogs menu coming soon!")
            # Here you would implement your dogs menu
            
        elif call.data == 'shop_menu':
            bot.answer_callback_query(call.id, "Shop menu coming soon!")
            # Here you would implement your shop menu
            
        elif call.data == 'change_language':
            bot.answer_callback_query(call.id, "Language menu coming soon!")
            # Here you would implement your language menu
            
        else:
            bot.answer_callback_query(call.id, "Unknown action")
    
    # Admin command - for testing
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        logger.info(f"Received /admin command from {message.from_user.username}")
        
        # This would check if the user is an admin
        is_admin = message.from_user.username in ['your_admin_username']
        
        if not is_admin:
            bot.reply_to(message, get_text('admin_message', message.from_user.language_code or 'en'))
            return
        
        # Admin functionality would go here
        bot.reply_to(message, "Admin command executed successfully.")
    
    # Generic message handler
    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        logger.info(f"Received message: {message.text} from {message.from_user.username}")
        
        # Here you would handle other messages or commands
        # For now, just echo back
        bot.reply_to(message, f"You said: {message.text}")
    
    logger.info("Starting bot polling...")
    
    # Start the bot
    bot.infinity_polling(logger_level=logging.DEBUG)
    
    logger.info("Bot stopped.")