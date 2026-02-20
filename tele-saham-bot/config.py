import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi Bot
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ISI_TOKEN_BOT_ANDA_DISINI')
BOT_USERNAME = os.getenv('BOT_USERNAME', '@NamaBotAnda')

# Database
DATABASE_NAME = 'saham_bot.db'

# API Keys (opsional, bisa pakai gratis)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')

# Admin
ADMIN_IDS = [123456789]  # Ganti dengan ID Telegram Anda

# Setting Bot
BOT_SETTINGS = {
    'max_watchlist': 10,
    'max_notifications': 5,
    'default_timeframe': '1D',
    'ai_model': 'gpt-3.5-turbo',
    'keep_alive': True
}
