#!/usr/bin/env python
import os
import telebot
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        exit(1)
    
    logger.info(f"Starting bot with token: {TELEGRAM_BOT_TOKEN[:5]}...")
    
    # Create the bot
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    
    # Define a /start handler
    @bot.message_handler(commands=['start'])
    def start(message):
        logger.info(f"Received /start command from {message.from_user.username}")
        bot.reply_to(message, "Hello! This is a simple test bot for DogTea Mining.")
    
    # Define a hello world handler
    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        logger.info(f"Received message: {message.text}")
        bot.reply_to(message, f"You said: {message.text}")
    
    logger.info("Starting bot polling...")
    
    # Start the bot (non-threaded mode)
    bot.infinity_polling(logger_level=logging.DEBUG)
    
    logger.info("Bot stopped.")