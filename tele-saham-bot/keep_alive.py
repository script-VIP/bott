from flask import Flask
from threading import Thread
import os
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return "🤖 Bot Saham Telegram Aktif 24/7!"

@app.route('/health')
def health():
    return {"status": "ok", "message": "Bot is running"}

@app.route('/stats')
def stats():
    return {"uptime": "24/7", "status": "active"}

def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Web server error: {e}")

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🌐 Web server started on port 8080 - Keep alive aktif!")
    print("📊 Cek status: http://localhost:8080/health")
