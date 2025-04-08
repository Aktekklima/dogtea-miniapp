
# DogteaMinerBot - GitHub + Render Setup

## Features

- Telegram Mining Bot with DOGTEA system
- Flask-based Mini App for Telegram WebApp integration
- TON token integration and referral
- Multilingual and game support

---

## How to Deploy on Render

1. **Fork this repo to your GitHub account**
2. Go to [https://render.com](https://render.com) and create a free account
3. Create a new Web Service:
   - Connect your GitHub
   - Select this repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `python web/server.py`
   - Environment: Python 3.10+
4. Make sure your Web Service is live at a public URL
5. Use the Render public URL as your Mini App URL on Telegram

---

## Starting Telegram Bot

To run the Telegram bot itself (not on Render), use:
```bash
python bot/main.py
```

You may host this with a separate VPS, Heroku, or Replit (not on Render).

---

Telegram:
- Chat: https://t.me/dogteachat
- Channel: https://t.me/dogteaminerbotnews
