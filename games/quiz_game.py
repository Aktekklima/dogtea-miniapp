import time
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.language_utils import get_text
from config import GAMES

# Sample quiz questions with dog theme
QUIZ_QUESTIONS = {
    'en': [
        {
            'question': 'Which dog breed is known for having a blue-black tongue?',
            'options': ['Husky', 'Chow Chow', 'Dalmatian', 'Poodle'],
            'correct': 1  # Chow Chow
        },
        {
            'question': 'What is the most popular dog breed in the world?',
            'options': ['Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'Bulldog'],
            'correct': 0  # Labrador Retriever
        },
        {
            'question': 'How many teeth does an adult dog have?',
            'options': ['22', '32', '42', '52'],
            'correct': 2  # 42
        },
        {
            'question': 'Which dog breed was originally bred to hunt lions?',
            'options': ['Great Dane', 'Rhodesian Ridgeback', 'Mastiff', 'St. Bernard'],
            'correct': 1  # Rhodesian Ridgeback
        },
        {
            'question': 'What is a group of pugs called?',
            'options': ['A pack', 'A grumble', 'A herd', 'A kennel'],
            'correct': 1  # A grumble
        }
    ],
    'tr': [
        {
            'question': 'Hangi köpek cinsi mavi-siyah dil ile bilinir?',
            'options': ['Husky', 'Chow Chow', 'Dalmaçyalı', 'Kaniş'],
            'correct': 1  # Chow Chow
        },
        {
            'question': 'Dünyanın en popüler köpek cinsi hangisidir?',
            'options': ['Labrador Retriever', 'Alman Çoban Köpeği', 'Golden Retriever', 'Bulldog'],
            'correct': 0  # Labrador Retriever
        },
        {
            'question': 'Yetişkin bir köpeğin kaç dişi vardır?',
            'options': ['22', '32', '42', '52'],
            'correct': 2  # 42
        },
        {
            'question': 'Hangi köpek cinsi aslan avlamak için yetiştirilmiştir?',
            'options': ['Great Dane', 'Rhodesian Ridgeback', 'Mastiff', 'St. Bernard'],
            'correct': 1  # Rhodesian Ridgeback
        },
        {
            'question': 'Bir grup pug ne olarak adlandırılır?',
            'options': ['Sürü', 'Homurdanma', 'Sürü', 'Kulübe'],
            'correct': 1  # Homurdanma (A grumble)
        }
    ],
    'ru': [
        {
            'question': 'Какая порода собак известна сине-черным языком?',
            'options': ['Хаски', 'Чау-чау', 'Далматинец', 'Пудель'],
            'correct': 1  # Чау-чау
        },
        {
            'question': 'Какая самая популярная порода собак в мире?',
            'options': ['Лабрадор-ретривер', 'Немецкая овчарка', 'Золотистый ретривер', 'Бульдог'],
            'correct': 0  # Лабрадор-ретривер
        },
        {
            'question': 'Сколько зубов у взрослой собаки?',
            'options': ['22', '32', '42', '52'],
            'correct': 2  # 42
        },
        {
            'question': 'Какую породу собак изначально разводили для охоты на львов?',
            'options': ['Немецкий дог', 'Родезийский риджбек', 'Мастиф', 'Сенбернар'],
            'correct': 1  # Родезийский риджбек
        },
        {
            'question': 'Как называется группа мопсов?',
            'options': ['Стая', 'Ворчание', 'Стадо', 'Питомник'],
            'correct': 1  # Ворчание (A grumble)
        }
    ],
    'ar': [
        {
            'question': 'أي سلالة كلاب تشتهر بلسانها الأزرق-الأسود؟',
            'options': ['هاسكي', 'تشاو تشاو', 'دلماسي', 'بودل'],
            'correct': 1  # تشاو تشاو
        },
        {
            'question': 'ما هي أكثر سلالة كلاب شعبية في العالم؟',
            'options': ['لابرادور ريتريفر', 'الراعي الألماني', 'جولدن ريتريفر', 'بولدوج'],
            'correct': 0  # لابرادور ريتريفر
        },
        {
            'question': 'كم عدد أسنان الكلب البالغ؟',
            'options': ['22', '32', '42', '52'],
            'correct': 2  # 42
        },
        {
            'question': 'أي سلالة كلاب تم تربيتها أصلاً لصيد الأسود؟',
            'options': ['جريت دان', 'روديسيان ريدجباك', 'ماستيف', 'سانت برنارد'],
            'correct': 1  # روديسيان ريدجباك
        },
        {
            'question': 'ماذا تسمى مجموعة من كلاب البج؟',
            'options': ['حزمة', 'تذمر', 'قطيع', 'مأوى'],
            'correct': 1  # تذمر (A grumble)
        }
    ]
}

async def start_quiz_game_session(update: Update, context: ContextTypes.DEFAULT_TYPE, language_code, callback=False):
    """Start a quiz game session."""
    # Make sure we have questions for this language
    if language_code not in QUIZ_QUESTIONS:
        language_code = 'en'  # Fall back to English
    
    # Select random question
    question_data = random.choice(QUIZ_QUESTIONS[language_code])
    
    # Set up game state
    context.user_data['quiz_game'] = {
        'question': question_data,
        'start_time': time.time(),
        'time_limit': GAMES['quiz']['time_limit']
    }
    
    # Create quiz keyboard
    keyboard = []
    for i, option in enumerate(question_data['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f"quiz_answer_{i}")])
    
    # Create game message
    game_text = get_text('quiz_game_question', language_code).format(
        question=question_data['question'],
        time_limit=GAMES['quiz']['time_limit']
    )
    
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

async def handle_quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callback queries."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    callback_data = query.data
    
    if 'quiz_game' not in context.user_data:
        await query.edit_message_text(get_text('game_expired', 'en'))
        return
    
    game_data = context.user_data['quiz_game']
    question_data = game_data['question']
    language_code = context.user_data.get('language_code', 'en')
    
    if callback_data.startswith("quiz_answer_"):
        # User answered
        selected_option = int(callback_data.split("_")[2])
        correct_option = question_data['correct']
        
        # Calculate response time
        response_time = time.time() - game_data['start_time']
        
        if response_time > game_data['time_limit']:
            # Too slow
            await query.edit_message_text(get_text('quiz_too_slow', language_code))
            context.user_data.pop('quiz_game', None)
            return
        
        if selected_option == correct_option:
            # Correct answer
            # Base reward
            reward = GAMES['quiz']['correct_reward']
            
            # Bonus for fast response
            time_bonus = max(0, game_data['time_limit'] - response_time)
            time_bonus_reward = min(GAMES['quiz']['bonus_time_reward'], time_bonus / 5)
            
            total_reward = reward + time_bonus_reward
            
            # Process reward
            # Import here to avoid circular imports
            from handlers.game_handlers import process_game_reward
            reward_text = await process_game_reward(update, context, 'quiz', total_reward)
            
            result_text = get_text('quiz_correct_answer', language_code).format(
                option=question_data['options'][correct_option],
                time=response_time,
                time_bonus=time_bonus_reward
            )
            
            await query.edit_message_text(f"{result_text}\n\n{reward_text}")
        else:
            # Wrong answer
            result_text = get_text('quiz_wrong_answer', language_code).format(
                selected=question_data['options'][selected_option],
                correct=question_data['options'][correct_option]
            )
            
            await query.edit_message_text(result_text)
        
        context.user_data.pop('quiz_game', None)
