from app import app  # noqa: F401
import logging
import os
import subprocess
import sys
import threading

logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_bot_process():
    """Start the bot process separately to avoid library conflicts"""
    logger.info("Starting simple bot process...")
    
    # Check if the token is available
    if not os.environ.get("TELEGRAM_BOT_TOKEN"):
        logger.error("Telegram bot token not found in environment variables!")
        return
    
    try:
        # Start the bot in a separate process using subprocess
        # This completely isolates the bot from the Flask app
        # to avoid any library conflicts
        subprocess.Popen([sys.executable, "simple_bot.py"])
        logger.info("Bot subprocess started successfully")
    except Exception as e:
        logger.error(f"Failed to start bot process: {e}")

if __name__ == "__main__":
    # Start the Telegram bot in a separate process
    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        # Start in a thread so it doesn't block the Flask app
        bot_thread = threading.Thread(target=start_bot_process)
        bot_thread.daemon = True
        bot_thread.start()
        logger.info("Bot thread started")
    else:
        logger.warning("Bot not started. TELEGRAM_BOT_TOKEN environment variable not set.")
    
    # Start the Flask web server in the main thread
    # We disable reloading to avoid spawning duplicate processes
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
