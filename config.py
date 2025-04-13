# Telegram Bot Configuration
import os
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7414241197:AAEDfQRkBIduU3-jC4ZIlVKEmx4s9RlkvLA")

# DOGTEA Token Configuration
INITIAL_DOGTEA_REWARD = 10  # Initial DOGTEA given to new users
MINING_RATE = {
    1: 0.5,  # Level 1 dog mining rate
    2: 1.0,  # Level 2 dog mining rate
    3: 1.5,  # Level 3 dog mining rate
    4: 2.0,  # Level 4 dog mining rate
    5: 3.0,  # Level 5 dog mining rate
}

# Dog Configuration
DOG_BREEDS = [
    "Labrador",
    "German Shepherd",
    "Bulldog",
    "Golden Retriever",
    "Siberian Husky",
    "Poodle",
    "Corgi",
    "Pug",
    "Beagle",
    "Chihuahua",
]

DOG_PRICING = {
    "Labrador": 5,
    "German Shepherd": 8,
    "Bulldog": 10,
    "Golden Retriever": 12,
    "Siberian Husky": 15,
    "Poodle": 20,
    "Corgi": 25,
    "Pug": 30,
    "Beagle": 40,
    "Chihuahua": 50,
}

# Game Configuration
GAMES = {
    "guess": {
        "max_attempts": 5,
        "reward": 2
    },
    "click": {
        "duration": 10,  # seconds
        "min_reward": 1,
        "max_reward": 5
    },
    "loot_box": {
        "min_reward": 1,
        "max_reward": 10
    },
    "quiz": {
        "time_limit": 15,  # seconds
        "correct_reward": 3,
        "bonus_time_reward": 1
    },
    "battle": {
        "base_reward": 5,
        "level_multiplier": 1.2
    }
}

# Game Limits
MAX_DAILY_GAMES = 2
MAX_AD_GAMES = 2

# XP Configuration
XP_REWARDS = {
    "daily_check_in": 10,
    "game_play": 5,
    "game_win": 10,
    "referral": 25,
    "dog_purchase": 20,
    "dog_upgrade": 15,
    "channel_join": 30,
    "group_participation": 5
}

# Supported Languages
SUPPORTED_LANGUAGES = ["tr", "en", "ru", "ar"]
DEFAULT_LANGUAGE = "en"

# TON Payment Configuration
TON_PROVIDER_URL = "https://ton.org/api"
TON_WALLET_ADDRESS = "UQB47bbmGWIk7QYYGJNiSSZIXDfVbKdmfdUlopEzYkx8HGYN"
