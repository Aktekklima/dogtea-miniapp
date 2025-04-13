import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Animation
from telegram.ext import ContextTypes
from utils.language_utils import get_text
from config import GAMES

async def open_loot_box(update: Update, context: ContextTypes.DEFAULT_TYPE, language_code, callback=False):
    """Start a loot box game session."""
    # Create loot box message
    game_text = get_text('loot_box_prompt', language_code)
    
    keyboard = [
        [
            InlineKeyboardButton("🎁", callback_data="loot_box_1"),
            InlineKeyboardButton("🎁", callback_data="loot_box_2"),
            InlineKeyboardButton("🎁", callback_data="loot_box_3")
        ]
    ]
    
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

async def handle_loot_box_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle loot box callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    language_code = context.user_data.get('language_code', 'en')
    
    if callback_data.startswith("loot_box_"):
        # User selected a loot box
        box_number = int(callback_data.split("_")[2])
        
        # Generate random reward
        min_reward = GAMES['loot_box']['min_reward']
        max_reward = GAMES['loot_box']['max_reward']
        reward = round(random.uniform(min_reward, max_reward), 1)
        
        # Process reward
        # Import here to avoid circular imports
        from handlers.game_handlers import process_game_reward
        reward_text = await process_game_reward(update, context, 'loot_box', reward)
        
        # Reveal the selected box content
        keyboard = []
        for i in range(1, 4):
            if i == box_number:
                # Show reward for selected box
                button_text = f"🎁 {reward} DOGTEA"
            else:
                # Show just the box for unselected ones
                button_text = "🎁"
            
            keyboard.append(InlineKeyboardButton(button_text, callback_data=f"loot_box_disabled_{i}"))
        
        result_text = get_text('loot_box_result', language_code).format(
            box_number=box_number,
            reward=reward
        )
        
        await query.edit_message_text(
            f"{result_text}\n\n{reward_text}",
            reply_markup=InlineKeyboardMarkup([keyboard])
        )
    
    elif callback_data.startswith("loot_box_disabled_"):
        # User clicked on an already revealed box - do nothing
        await query.answer(get_text('loot_box_already_opened', language_code))
