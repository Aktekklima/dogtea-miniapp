import logging
import random
import string
from telegram import Update, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from models import User, Dog, Transaction
from app import db
from utils.user_utils import get_or_create_user
from utils.dog_utils import create_new_dog
from utils.language_utils import get_text
from config import DOG_PRICING, XP_REWARDS

logger = logging.getLogger(__name__)

async def buy_dog_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle dog purchase button callback."""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    callback_data = query.data
    breed = callback_data.replace("buy_dog_", "")
    
    # Get dog price
    price = DOG_PRICING.get(breed, 5)
    
    # Create payment invoice
    title = get_text('dog_purchase_title', language_code).format(breed=breed)
    description = get_text('dog_purchase_description', language_code).format(
        breed=breed,
        price=price
    )
    
    # Generate a unique invoice payload
    payload = f"dog_{breed}_{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
    
    # TON currency is "TON"
    currency = "TON"
    
    # Price in smallest units (TON nanocoins)
    price_in_nanocoins = int(price * 1_000_000_000)
    
    # Create labeled price
    prices = [LabeledPrice(breed, price_in_nanocoins)]
    
    try:
        # In real implementation, use Tonkeeper API for payments
        # For now, simulate successful payment and dog creation
        
        # Create confirmation dialog instead of real payment
        confirm_text = get_text('confirm_purchase', language_code).format(
            breed=breed,
            price=price
        )
        
        keyboard = [
            [
                InlineKeyboardButton(
                    get_text('confirm_button', language_code),
                    callback_data=f"confirm_dog_{breed}"
                ),
                InlineKeyboardButton(
                    get_text('cancel_button', language_code),
                    callback_data="shop_menu"
                )
            ]
        ]
        
        await query.edit_message_text(
            confirm_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        
        error_text = get_text('payment_error', language_code)
        await query.edit_message_text(error_text)

async def process_ton_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process successful TON payment."""
    user = update.effective_user
    db_user = get_or_create_user(user.id, user.username, user.first_name, user.last_name, user.language_code)
    language_code = db_user.language_code
    
    successful_payment = update.message.successful_payment
    
    # Extract information from payment payload
    payload = successful_payment.invoice_payload
    total_amount = successful_payment.total_amount / 1_000_000_000  # Convert from nanocoins to TON
    
    if payload.startswith("dog_"):
        # Dog purchase
        _, breed, _ = payload.split("_", 2)
        
        # Generate a random name for the dog
        dog_names = ["Buddy", "Max", "Charlie", "Rocky", "Cooper", "Duke", "Bear", "Teddy", "Tucker", "Winston"]
        name = random.choice(dog_names)
        
        # Create new dog
        dog = create_new_dog(db_user.id, name, breed)
        
        # Record transaction
        transaction = Transaction(
            user_id=db_user.id,
            type="dog_purchase",
            amount=total_amount,
            currency="TON",
            description=f"Purchase of {breed} dog named {name}",
            tx_hash=successful_payment.provider_payment_charge_id
        )
        db.session.add(transaction)
        
        # Add XP for dog purchase
        db_user.add_xp(XP_REWARDS['dog_purchase'])
        
        db.session.commit()
        
        # Send confirmation message
        confirmation_text = get_text('purchase_successful', language_code).format(
            name=name,
            breed=breed
        )
        
        await update.message.reply_text(confirmation_text)
