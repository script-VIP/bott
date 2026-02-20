#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 BOT SAHAM TELEGRAM - MAIN BOT
Multi OS Support | Auto Alive | AI Integration
"""

import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Import modul internal
from config import BOT_TOKEN, BOT_SETTINGS
from database import db
from saham_handler import SahamHandler
from ai_handler import AIHandler
from keep_alive import keep_alive

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inisialisasi handler
saham = SahamHandler()
ai = AIHandler()

# ============================================
# MENU UTAMA
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start"""
    user = update.effective_user
    
    # Simpan user ke database
    db.add_user(user.id, user.username, user.first_name)
    
    # Pesan selamat datang
    welcome_text = f"""
🤖 *BOT INFORMASI SAHAM INDONESIA*
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Halo *{user.first_name}*! Selamat datang di Bot Saham Indonesia!

📌 *LAYANAN BOT*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Tanya AI seputar saham
🔍 Cari informasi saham terkini
📈 Analisis teknikal & fundamental
💰 Screening saham berdasarkan kriteria
🔔 Notifikasi harga & watchlist
    """
    
    # Keyboard menu utama
    keyboard = [
        [
            InlineKeyboardButton("💬 Tanya AI", callback_data="ai_start"),
            InlineKeyboardButton("📈 Analisis", callback_data="analisis_menu")
        ],
        [
            InlineKeyboardButton("🔍 Cari Saham", callback_data="cari_saham"),
            InlineKeyboardButton("📊 Screening", callback_data="screening_menu")
        ],
        [
            InlineKeyboardButton("💰 Gainer/Loser", callback_data="gainer_loser"),
            InlineKeyboardButton("📈 IHSG", callback_data="ihsg")
        ],
        [
            InlineKeyboardButton("🔔 Notifikasi", callback_data="notifikasi_menu"),
            InlineKeyboardButton("⭐ Watchlist", callback_data="watchlist_menu")
        ],
        [
            InlineKeyboardButton("❓ Bantuan", callback_data="bantuan"),
            InlineKeyboardButton("👤 Profil", callback_data="profil")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ============================================
# TANYA AI
# ============================================

async def ai_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu Tanya AI"""
    query = update.callback_query
    await query.answer()
    
    text = """
💬 *TANYA AI SEPUTAR SAHAM*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Halo! Saya AI Assistant siap membantu Anda.

📝 *HAL YANG BISA DITANYAKAN:*
• Analisis teknikal (RSI, MACD, MA, dll)
• Analisis fundamental (P/E, ROE, valuasi)
• Interpretasi chart & pola
• Strategi trading & manajemen risiko
• Berita & sentimen pasar
• Edukasi saham untuk pemula

💡 *CONTOH PERTANYAAN:*
• "Apa artinya RSI 34.7 pada BBCA?"
• "Jelaskan pola double bottom"
• "Bagaimana prospek saham perbankan 2026?"
• "Apa indikator terbaik untuk day trade?"

✍️ *Silakan ketik pertanyaan Anda:*
    """
    
    keyboard = [
        [InlineKeyboardButton("❓ Contoh Pertanyaan", callback_data="ai_examples")],
        [InlineKeyboardButton("📊 Analisis Saham BBCA", callback_data="saham:BBCA")],
        [InlineKeyboardButton("📈 Cek IHSG", callback_data="ihsg")],
        [InlineKeyboardButton("🔙 Kembali", callback_data="start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
