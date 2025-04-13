import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.language_utils import get_text
from config import GAMES

async def start_guess_game_session(update: Update, context: ContextTypes.DEFAULT_TYPE, language_code, callback=False):
    """Start a guessing game session."""
    # Generate a random number between 1 and 100
    target_number = random.randint(1, 100)
    context.user_data['guess_game'] = {
        'target': target_number,
        'attempts': 0,
        'max_attempts': GAMES['guess']['max_attempts']
    }
    
    # Create game message
    game_text = get_text('guess_game_start', language_code).format(
        max_attempts=GAMES['guess']['max_attempts']
    )
    
    if callback:
        # Called from callback query
        query = update.callback_query
        await query.edit_message_text(
            game_text,
            reply_markup=create_number_keyboard(language_code)
        )
    else:
        # Called from command
        await update.message.reply_text(
            game_text,
            reply_markup=create_number_keyboard(language_code)
        )

def create_number_keyboard(language_code):
    """Create a keyboard with number ranges for guessing."""
    keyboard = [
        [
            InlineKeyboardButton("1-25", callback_data="guess_range_1_25"),
            InlineKeyboardButton("26-50", callback_data="guess_range_26_50")
        ],
        [
            InlineKeyboardButton("51-75", callback_data="guess_range_51_75"),
            InlineKeyboardButton("76-100", callback_data="guess_range_76_100")
        ],
        [
            InlineKeyboardButton(get_text('cancel_button', language_code), callback_data="cancel_game")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_specific_number_keyboard(start, end, language_code):
    """Create a keyboard with specific numbers for the selected range."""
    keyboard = []
    row = []
    
    for i in range(start, end + 1):
        row.append(InlineKeyboardButton(str(i), callback_data=f"guess_{i}"))
        if len(row) == 5:  # 5 numbers per row
            keyboard.append(row)
            row = []
    
    if row:  # Add remaining numbers
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(get_text('back_button', language_code), callback_data="guess_back_to_ranges")
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def handle_guess_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle guess game callback queries."""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    user = update.effective_user
    
    if 'guess_game' not in context.user_data:
        await query.edit_message_text(get_text('game_expired', 'en'))
        return
    
    game_data = context.user_data['guess_game']
    target = game_data['target']
    language_code = context.user_data.get('language_code', 'en')
    
    if callback_data == "cancel_game":
        await query.edit_message_text(get_text('game_cancelled', language_code))
        context.user_data.pop('guess_game', None)
        return
    
    if callback_data == "guess_back_to_ranges":
        await query.edit_message_text(
            get_text('guess_game_prompt', language_code).format(
                attempts=game_data['attempts'],
                max_attempts=game_data['max_attempts']
            ),
            reply_markup=create_number_keyboard(language_code)
        )
        return
    
    if callback_data.startswith("guess_range_"):
        # User selected a range
        _, _, start, end = callback_data.split("_")
        start, end = int(start), int(end)
        
        await query.edit_message_text(
            get_text('guess_game_select_number', language_code).format(
                start=start,
                end=end,
                attempts=game_data['attempts'],
                max_attempts=game_data['max_attempts']
            ),
            reply_markup=create_specific_number_keyboard(start, end, language_code)
        )
        return
    
    if callback_data.startswith("guess_"):
        # User made a specific guess
        guess = int(callback_data.replace("guess_", ""))
        game_data['attempts'] += 1
        
        if guess == target:
            # Correct guess!
            reward = GAMES['guess']['reward']
            # Import here to avoid circular imports
            from handlers.game_handlers import process_game_reward
            reward_text = await process_game_reward(update, context, 'guess', reward)
            
            success_text = get_text('guess_game_win', language_code).format(
                target=target,
                attempts=game_data['attempts']
            )
            
            await query.edit_message_text(f"{success_text}\n\n{reward_text}")
            context.user_data.pop('guess_game', None)
            return
        
        # Wrong guess
        hint = "higher" if target > guess else "lower"
        hint_text = get_text(f'guess_{hint}', language_code)
        
        if game_data['attempts'] >= game_data['max_attempts']:
            # Game over
            fail_text = get_text('guess_game_lose', language_code).format(
                target=target
            )
            
            await query.edit_message_text(fail_text)
            context.user_data.pop('guess_game', None)
            return
        
        # Continue game
        continue_text = get_text('guess_game_continue', language_code).format(
            guess=guess,
            hint=hint_text,
            attempts=game_data['attempts'],
            max_attempts=game_data['max_attempts']
        )
        
        await query.edit_message_text(
            continue_text,
            reply_markup=create_number_keyboard(language_code)
        )
