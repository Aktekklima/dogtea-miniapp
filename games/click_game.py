import time
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.language_utils import get_text
from config import GAMES

async def start_click_game_session(update: Update, context: ContextTypes.DEFAULT_TYPE, language_code, callback=False):
    """Start a clicking speed game session."""
    # Set up game state
    context.user_data['click_game'] = {
        'clicks': 0,
        'start_time': time.time(),
        'duration': GAMES['click']['duration'],
        'active': True
    }
    
    # Create game message
    game_text = get_text('click_game_start', language_code).format(
        duration=GAMES['click']['duration']
    )
    
    keyboard = [[
        InlineKeyboardButton(
            get_text('click_button', language_code), 
            callback_data="click_button"
        )
    ]]
    
    if callback:
        # Called from callback query
        query = update.callback_query
        await query.edit_message_text(
            game_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        # Called from command
        await update.message.reply_text(
            game_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_click_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle click game callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    
    if 'click_game' not in context.user_data:
        await query.edit_message_text(get_text('game_expired', 'en'))
        return
    
    game_data = context.user_data['click_game']
    language_code = context.user_data.get('language_code', 'en')
    
    if not game_data.get('active', False):
        await query.edit_message_text(get_text('game_expired', language_code))
        return
    
    if callback_data == "click_button":
        current_time = time.time()
        elapsed_time = current_time - game_data['start_time']
        
        if elapsed_time <= game_data['duration']:
            # Valid click within time limit
            game_data['clicks'] += 1
            
            # Update the button text with current clicks
            remaining_time = max(0, game_data['duration'] - elapsed_time)
            
            if remaining_time > 0:
                # Game still active
                keyboard = [[
                    InlineKeyboardButton(
                        f"{game_data['clicks']} {get_text('clicks', language_code)} - {remaining_time:.1f}s", 
                        callback_data="click_button"
                    )
                ]]
                
                await query.edit_message_text(
                    get_text('click_game_progress', language_code).format(
                        clicks=game_data['clicks'],
                        remaining=remaining_time
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                # Time's up
                game_data['active'] = False
                
                # Calculate reward based on clicks
                clicks = game_data['clicks']
                min_reward = GAMES['click']['min_reward']
                max_reward = GAMES['click']['max_reward']
                
                # Scale reward based on clicks (more clicks = more reward)
                # Simple formula: min_reward + (clicks / 10) up to max_reward
                reward = min(max_reward, min_reward + (clicks / 10))
                
                # Import here to avoid circular imports
                from handlers.game_handlers import process_game_reward
                reward_text = await process_game_reward(update, context, 'click', reward)
                
                result_text = get_text('click_game_end', language_code).format(
                    clicks=clicks,
                    duration=game_data['duration']
                )
                
                await query.edit_message_text(f"{result_text}\n\n{reward_text}")
                context.user_data.pop('click_game', None)
        else:
            # Time's up
            game_data['active'] = False
            
            result_text = get_text('click_game_end', language_code).format(
                clicks=game_data['clicks'],
                duration=game_data['duration']
            )
            
            await query.edit_message_text(result_text)
            context.user_data.pop('click_game', None)
