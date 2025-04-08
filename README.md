
# DogteaMinerBot

DogteaMinerBot is an advanced and beautifully designed Telegram mining and game bot, inspired by the popular CatteaBot. It allows users to mine $DOGTEA tokens, play mini-games, upgrade dogs, and participate in PvP battles — all in a colorful and engaging interface.

## Features

- Token mining system with hourly earnings
- Interactive start screen with a “Play” button
- User profile with XP, level, and rank system
- Mining cards (Lv1–Lv5) that increase mining power
- Multi-language support (TR, EN, AR, RU, etc.)
- Dog strengthening and evolution system
- Dog vs battle system (DOGTEA betting)
- Mini-games: Clicker, Quiz, Guess Game, Luck Box
- Referral system with bonus tokens
- In-bot shop (upgrade, cards, premium)
- Airdrop system and ad-based rewards
- WebApp MiniApp interface (like Cattea)
- TON-based payment system (Tonkeeper link)
- Support for Render and GitHub deployment

## Setup

### Environment Variables Required

Make sure to set these in your Render project or `.env` file:

```env
BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://yourdomain.onrender.com
OWNER_ID=your_telegram_id
TON_WALLET=your_ton_wallet_address
```

### How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run bot: `python main.py`

## Deployment

This bot is compatible with **Render + GitHub**. Just connect your GitHub repo, add your environment variables, and deploy.

## License

MIT License
