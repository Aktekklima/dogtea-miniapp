import logging
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models import User, Transaction
from app import db
from utils.user_utils import get_or_create_user
from utils.language_utils import get_text
from utils.token_utils import add_dogtea_reward
from games.guess_game import start_guess_game_session
from games.click_game import start_click_game_session
from games.loot_box import open_loot_box
from games.quiz_game import start_quiz_game_session
from config import GAMES, XP_REWARDS

logger = logging.getLogger(__name__)

async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /play command - show available games to play."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
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
        
        await update.message.reply_text(
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
        ]
    ]
    
    await update.message.reply_text(
        games_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_guess_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the number guessing game."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Check if the user can play more games today
    can_play = db_user.can_play_game()
    
    if not can_play:
        await update.message.reply_text(get_text('no_games_left', language_code))
        return
    
    # Reduce available games and track play
    db_user.games_left_today -= 1
    db_user.games_played_today += 1
    db.session.commit()
    
    # Award XP for playing a game
    db_user.add_xp(XP_REWARDS['game_play'])
    
    # Start the guessing game
    await start_guess_game_session(update, context, language_code)

async def start_click_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the clicking speed game."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Check if the user can play more games today
    can_play = db_user.can_play_game()
    
    if not can_play:
        await update.message.reply_text(get_text('no_games_left', language_code))
        return
    
    # Reduce available games and track play
    db_user.games_left_today -= 1
    db_user.games_played_today += 1
    db.session.commit()
    
    # Award XP for playing a game
    db_user.add_xp(XP_REWARDS['game_play'])
    
    # Start the clicking game
    await start_click_game_session(update, context, language_code)

async def start_loot_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the loot box game."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Check if the user can play more games today
    can_play = db_user.can_play_game()
    
    if not can_play:
        await update.message.reply_text(get_text('no_games_left', language_code))
        return
    
    # Reduce available games and track play
    db_user.games_left_today -= 1
    db_user.games_played_today += 1
    db.session.commit()
    
    # Award XP for playing a game
    db_user.add_xp(XP_REWARDS['game_play'])
    
    # Open the loot box
    await open_loot_box(update, context, language_code)

async def start_quiz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the quiz game."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Check if the user can play more games today
    can_play = db_user.can_play_game()
    
    if not can_play:
        await update.message.reply_text(get_text('no_games_left', language_code))
        return
    
    # Reduce available games and track play
    db_user.games_left_today -= 1
    db_user.games_played_today += 1
    db.session.commit()
    
    # Award XP for playing a game
    db_user.add_xp(XP_REWARDS['game_play'])
    
    # Start the quiz game
    await start_quiz_game_session(update, context, language_code)

async def process_game_reward(update: Update, context: ContextTypes.DEFAULT_TYPE, game_type, reward_amount):
    """Process reward for winning a game."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    # Add XP for winning a game
    level_ups = db_user.add_xp(XP_REWARDS['game_win'])
    
    # Add DOGTEA tokens
    add_dogtea_reward(db_user, reward_amount, f"{game_type}_reward")
    
    # Create notification message
    reward_text = get_text('game_reward', language_code).format(
        reward_amount=reward_amount,
        new_balance=db_user.dogtea_balance
    )
    
    if level_ups > 0:
        reward_text += "\n\n" + get_text('level_up', language_code).format(
            new_level=db_user.level
        )
    
    return reward_text
