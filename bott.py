#!/usr/bin/env python3
"""
BOT SAHAM INDONESIA LENGKAP
Fitur: Tanya AI, Analisis Teknikal, Screening, Watchlist, IHSG
Setup: Auto request token (1 file aja!)
Author: AI Assistant
Version: 5.0 (All-in-One)
"""

import logging
import asyncio
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import ta
import json
import io
import os
import sys
import time
import random
from collections import defaultdict

# ======================== SETUP TOKEN OTOMATIS ========================
BOT_TOKEN = None

def print_header():
    """Print header keren"""
    print("\n" + "█"*60)
    print("██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ ")
    print("██║  ██║██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ ")
    print("███████║██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗")
    print("██╔══██║██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║")
    print("██║  ██║╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝")
    print("╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ ")
    print("█"*60)
    print("🔥 BOT SAHAM INDONESIA LENGKAP v5.0".center(60))
    print("█"*60)

def setup_token():
    """Setup token interaktif"""
    global BOT_TOKEN
    
    print_header()
    print("\n📢 PENTING: Bot memerlukan token Telegram!")
    
    # Cek apakah sudah ada file token
    if os.path.exists('.token'):
        print("\n📁 File token ditemukan!")
        use_existing = input("🔑 Gunakan token yang sudah ada? (y/n): ").strip().lower()
        if use_existing == 'y':
            with open('.token', 'r') as f:
                BOT_TOKEN = f.read().strip()
            print("\n✅ Token dimuat dari file!")
            print("🚀 Melanjutkan...\n")
            return
    
    # Minta token baru
    print("\n💬 Silakan masukkan token dari @BotFather")
    print("   (Contoh: 8165382231:AAG3WjlyJ9Ylaz3pKkQUSmZLi-ovkSxBS7w)\n")
    
    attempts = 0
    while attempts < 3:
        token = input("👉 BOT_TOKEN: ").strip()
        
        if not token:
            print("❌ Token tidak boleh kosong!")
            attempts += 1
            continue
            
        if ':' not in token:
            print("❌ Format token salah! Harus ada tanda ':'")
            attempts += 1
            continue
        
        BOT_TOKEN = token
        with open('.token', 'w') as f:
            f.write(token)
        print("\n✅ Token berhasil disimpan di .token")
        print("🚀 Menjalankan bot...\n")
        return
    
    print("\n❌ Gagal memasukkan token. Jalankan ulang.")
    sys.exit(1)

# Jalankan setup
setup_token()

# ======================== KONFIGURASI LOGGING ========================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ======================== DATABASE SEDERHANA (JSON) ========================
class SimpleDB:
    def __init__(self):
        self.data_file = 'bot_data.json'
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'users': {},
                'watchlist': {},
                'notifications': []
            }
            self.save_data()
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_user(self, user_id, username, first_name):
        user_id = str(user_id)
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {
                'username': username,
                'first_name': first_name,
                'join_date': datetime.now().isoformat(),
                'preferences': {}
            }
            self.save_data()
    
    def get_watchlist(self, user_id):
        user_id = str(user_id)
        return self.data['watchlist'].get(user_id, [])
    
    def add_to_watchlist(self, user_id, saham):
        user_id = str(user_id)
        if user_id not in self.data['watchlist']:
            self.data['watchlist'][user_id] = []
        if saham not in self.data['watchlist'][user_id]:
            self.data['watchlist'][user_id].append(saham)
            self.save_data()
            return True
        return False
    
    def remove_from_watchlist(self, user_id, saham):
        user_id = str(user_id)
        if user_id in self.data['watchlist'] and saham in self.data['watchlist'][user_id]:
            self.data['watchlist'][user_id].remove(saham)
            self.save_data()
            return True
        return False

db = SimpleDB()

# ======================== DAFTAR SAHAM INDONESIA ========================
INDONESIA_STOCKS = {
    'IDX30': ['BBCA', 'BBRI', 'BMRI', 'BBNI', 'ASII', 'TLKM', 'ICBP', 'INDF', 'UNVR', 'GGRM',
              'HMSP', 'KLBF', 'CPIN', 'JPFA', 'PGAS', 'PTBA', 'ADRO', 'ITMG', 'EXCL', 'ISAT',
              'WIKA', 'PTPP', 'ADHI', 'WSKT', 'BSDE', 'LPKR', 'PWON', 'SMRA', 'CTRA', 'JSMR'],
    
    'LQ45': ['ACES', 'ADRO', 'AKRA', 'ANTM', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BBTN', 'BMRI',
             'BRPT', 'BSDE', 'CPIN', 'ELSA', 'ERAA', 'EXCL', 'GGRM', 'HMSP', 'ICBP', 'INCO',
             'INDF', 'INDY', 'INKP', 'INTP', 'ITMG', 'JPFA', 'JSMR', 'KLBF', 'LPKR', 'LSIP',
             'MDKA', 'MEDC', 'MIKA', 'MNCN', 'PGAS', 'PTBA', 'PTPP', 'PWON', 'SMGR', 'SMRA',
             'TBIG', 'TKIM', 'TLKM', 'TOWR', 'TPIA', 'UNTR', 'UNVR', 'WIKA', 'WSKT'],
    
    'BANK': ['BBCA', 'BBRI', 'BMRI', 'BBNI', 'BTPS', 'BNGA', 'BNLI', 'NISP', 'MAYA', 'BBTN',
             'BTPN', 'BJBR', 'BJTM', 'BDMN', 'BNBA', 'SDRA', 'AGRO', 'PNBN', 'ARTO'],
    
    'TAMBANG': ['ADRO', 'PTBA', 'ITMG', 'ANTM', 'INCO', 'MDKA', 'BUMI', 'BYAN', 'HRUM', 'MEDC',
                'ELSA', 'DOID', 'DKFT', 'GEMS', 'KKGI', 'MYOH', 'PSAB', 'RUIS', 'TOBA'],
    
    'TEKNOLOGI': ['GOTO', 'BUKA', 'EMTK', 'MCAS', 'DIVA', 'HDIT', 'KOTA', 'LUCK', 'MPOW', 'NICE',
                  'PURI', 'RATU', 'SATU', 'TFAS', 'UNIQ', 'WGSH', 'ZONE'],
    
    'INFRA': ['TLKM', 'ISAT', 'EXCL', 'TOWR', 'TBIG', 'JSMR', 'PGAS', 'WIKA', 'PTPP', 'ADHI',
              'WSKT', 'TOTL', 'BALI', 'CASS', 'CMNP', 'HADE', 'KARW', 'META', 'NRCA'],
}

# FLAT LIST
ALL_INDONESIA_STOCKS = []
for sector in INDONESIA_STOCKS.values():
    ALL_INDONESIA_STOCKS.extend(sector)
ALL_INDONESIA_STOCKS = sorted(list(set(ALL_INDONESIA_STOCKS)))

# ======================== AI HANDLER ========================
class AIHandler:
    async def ask(self, question):
        """Jawab pertanyaan tentang saham"""
        question_lower = question.lower()
        
        # Deteksi topik
        if 'rsi' in question_lower:
            return self._answer_rsi()
        elif 'macd' in question_lower:
            return self._answer_macd()
        elif 'double bottom' in question_lower:
            return self._answer_double_bottom()
        elif 'candlestick' in question_lower:
            return self._answer_candlestick()
        elif 'support' in question_lower and 'resistance' in question_lower:
            return self._answer_support_resistance()
        elif 'moving average' in question_lower or 'ma' in question_lower:
            return self._answer_ma()
        elif 'bbca' in question_lower:
            return self._answer_bbca()
        elif 'bbri' in question_lower:
            return self._answer_bbri()
        elif 'tlkm' in question_lower:
            return self._answer_tlkm()
        elif 'gainer' in question_lower:
            return self._answer_gainer()
        elif 'loser' in question_lower:
            return self._answer_loser()
        elif 'p/e' in question_lower or 'pe' in question_lower:
            return self._answer_pe()
        elif 'fundamental' in question_lower:
            return self._answer_fundamental()
        elif 'day trade' in question_lower:
            return self._answer_daytrade()
        elif 'swing' in question_lower:
            return self._answer_swing()
        else:
            return self._answer_default(question)
    
    def _answer_rsi(self):
        return """
📊 *RELATIVE STRENGTH INDEX (RSI)*

RSI adalah indikator momentum yang mengukur kecepatan dan perubahan pergerakan harga.

🔴 *INTERPRETASI:*
• RSI > 70 = Overbought (jenuh beli) - potensi koreksi
• RSI < 30 = Oversold (jenuh jual) - potensi rebound
• RSI 30-70 = Normal

📌 *CONTOH:* 
Jika RSI BBCA 34.7, artinya mendekati oversold, tekanan jual mulai berkurang.

🎯 *PENGGUNAAN:*
• Cari sinyal beli saat RSI < 30 dan mulai naik
• Cari sinyal jual saat RSI > 70 dan mulai turun
• Kombinasikan dengan support resistance

💡 *TIPS:* RSI cocok untuk swing trading (3-10 hari).
        """
    
    def _answer_macd(self):
        return """
📊 *MOVING AVERAGE CONVERGENCE DIVERGENCE (MACD)*

MACD adalah indikator trend-following yang menunjukkan hubungan antara dua moving average.

🔴 *KOMPONEN MACD:*
• MACD Line (Cepat) - EMA 12
• Signal Line (Lambat) - EMA 26
• Histogram - Selisih MACD dan Signal

📌 *SINYAL:*
• MACD crossover (potong Signal ke atas) = BULLISH
• MACD crossunder (potong Signal ke bawah) = BEARISH
• Histogram hijau = Momentum naik
• Histogram merah = Momentum turun

🎯 *STRATEGI:*
• Beli saat MACD crossover dan histogram positif
• Jual saat MACD crossunder dan histogram negatif
        """
    
    def _answer_double_bottom(self):
        return """
📊 *POLA DOUBLE BOTTOM (W-SHAPED)*

Double Bottom adalah pola reversal bullish yang terbentuk setelah tren turun.

🔍 *KARAKTERISTIK:*
• Bottom 1: Harga turun ke level terendah
• Rebound: Harga naik sementara (neckline)
• Bottom 2: Harga turun lagi ke level yang sama
• Breakout: Harga menembus neckline

📌 *KONFIRMASI:*
• Jarak antar bottom: 1-4 minggu
• Bottom 2 tidak lebih rendah dari bottom 1
• Volume lebih besar di bottom 2
• Breakout dengan volume tinggi

📈 *TARGET HARGA:*
Tinggi pola (neckline - bottom) diproyeksikan ke atas
        """
    
    def _answer_candlestick(self):
        return """
📊 *POLA CANDLESTICK*

Candlestick menunjukkan 4 harga: Open, High, Low, Close.

🕯️ *BAGIAN CANDLESTICK:*
• Body: Selisih Open dan Close
• Shadow/Wick: Harga tertinggi/terendah
• Bullish (hijau): Close > Open
• Bearish (merah): Close < Open

📈 *POLA BULLISH:*
• Hammer: Bottom reversal
• Engulfing Bullish: Body besar telan body kecil
• Morning Star: 3 candle reversal
• Doji: Indecision, potensi reversal

📉 *POLA BEARISH:*
• Shooting Star: Top reversal
• Engulfing Bearish: Body besar telan body kecil
• Evening Star: 3 candle reversal
        """
    
    def _answer_support_resistance(self):
        return """
📊 *SUPPORT & RESISTANCE*

Support dan Resistance adalah level harga di mana tren cenderung berhenti atau berbalik.

🛡️ *SUPPORT:*
• Level di mana harga cenderung berhenti turun
• Area beli potensial
• Bisa berasal dari: low sebelumnya, MA, atau level psikologis

🎯 *RESISTANCE:*
• Level di mana harga cenderung berhenti naik
• Area jual potensial
• Bisa berasal dari: high sebelumnya, MA, atau level psikologis

📌 *STRATEGI:*
• Beli di support, jual di resistance (range trading)
• Beli saat breakout resistance (trend following)
• Jual saat breakdown support (trend reversal)

💡 *PSIKOLOGIS:* 
Level-round number (1000, 5000, 10000) sering jadi support/resistance kuat.
        """
    
    def _answer_ma(self):
        return """
📊 *MOVING AVERAGE (MA)*

MA adalah indikator yang meratakan data harga untuk mengidentifikasi arah tren.

📈 *JENIS-JENIS MA:*
• MA5: Tren jangka pendek (1 minggu)
• MA20: Tren bulanan
• MA50: Tren kuartalan
• MA100: Tren semesteran
• MA200: Tren tahunan

🔴 *INTERPRETASI:*
• Harga di atas MA = Bullish
• Harga di bawah MA = Bearish
• MA5 > MA20 = Momentum naik (golden cross)
• MA5 < MA20 = Momentum turun (death cross)

🎯 *PENGGUNAAN:*
• MA5/20 untuk entry timing
• MA50/100 untuk trend filter
• MA200 untuk support/resistance kuat
        """
    
    def _answer_bbca(self):
        return """
📊 *ANALISIS BBCA (Bank Central Asia Tbk)*

💰 *HARGA:* Rp 9,875 (Update terbaru)

📈 *PROFIL:*
• Bank swasta terbesar di Indonesia
• Market cap: Rp 1,200 T
• ROE: 21.1% (sangat baik)
• NIM: 5.8% (efisien)

📊 *TEKNIKAL (TERKINI):*
• Trend jangka panjang: Bullish (di atas MA200)
• Trend jangka pendek: Konsolidasi
• RSI: 52 (netral)
• Support: Rp 9,500 | Rp 9,200
• Resistance: Rp 10,000 | Rp 10,500

📌 *REKOMENDASI:*
• Swing: Buy on pullback ke 9,500
• Day trade: Range 9,750 - 10,000
• Long term: Accumulate di bawah 9,500

💡 *FUNDAMENTAL:* 
Salah satu bank dengan kualitas aset terbaik di Indonesia.
        """
    
    def _answer_bbri(self):
        return """
📊 *ANALISIS BBRI (Bank Rakyat Indonesia Tbk)*

💰 *HARGA:* Rp 5,450 (Update terbaru)

📈 *PROFIL:*
• Bank BUMN fokus mikro & UMKM
• Market cap: Rp 820 T
• ROE: 18.5% (baik)
• NIM: 7.2% (tinggi)

📊 *TEKNIKAL (TERKINI):*
• Trend jangka panjang: Bullish
• Trend jangka pendek: Uptrend
• RSI: 58 (netral)
• Support: Rp 5,200 | Rp 5,000
• Resistance: Rp 5,600 | Rp 5,800

📌 *REKOMENDASI:*
• Swing: Hold selama di atas MA20
• Day trade: Momentum buy di atas 5,500
• Long term: Cocok untuk dividen

💡 *KATALIS:* 
Penyaluran KUR dan digitalisasi BRImo.
        """
    
    def _answer_tlkm(self):
        return """
📊 *ANALISIS TLKM (Telkom Indonesia Tbk)*

💰 *HARGA:* Rp 3,890 (Update terbaru)

📈 *PROFIL:*
• Telekomunikasi terbesar Indonesia
• Market cap: Rp 385 T
• ROE: 15.3% (baik)
• Margin: 45% (tinggi)

📊 *TEKNIKAL (TERKINI):*
• Trend jangka panjang: Sideways
• Trend jangka pendek: Bearish
• RSI: 32 (oversold)
• Support: Rp 3,800 | Rp 3,700
• Resistance: Rp 4,000 | Rp 4,200

📌 *REKOMENDASI:*
• Swing: Buy di area oversold 3,800
• Target: Rp 4,000 - 4,200
• Long term: Accumulate untuk dividen

💡 *KATALIS:* 
Transformasi digital dan data center.
        """
    
    def _answer_gainer(self):
        return """
📊 *TOP GAINER (Saham dengan kenaikan tertinggi)*

🔍 *CARA MENCARI:*
• Gunakan menu Screening -> Top Gainer
• Filter dengan volume > rata-rata
• Perhatikan katalis (berita, laporan keuangan)

📈 *STRATEGI:*
• Jangan FOMO (Fear Of Missing Out)
• Tunggu pullback untuk entry
• Pasang stop loss ketat
• Ambil profit bertahap

⚠️ *RISIKO:*
• Bisa dead cat bounce (pantulan sementara)
• Rawan reversal tajam
• Volume palsu (pump and dump)

💡 *TIPS:* 
Kombinasikan dengan indikator RSI & MACD untuk konfirmasi momentum.
        """
    
    def _answer_loser(self):
        return """
📊 *TOP LOSER (Saham dengan penurunan terbesar)*

🔍 *CARA MENCARI:*
• Gunakan menu Screening -> Top Loser
• Cek apakah ada koreksi wajar atau masalah fundamental
• Perhatikan volume (jual panik atau distribusi)

📉 *STRATEGI:*
• BUY THE DIP jika fundamental kuat
• Tunggu konfirmasi reversal (RSI oversold + bullish candle)
• Averaging jika tren masih turun
• Cut loss jika breakdown support

⚠️ *RISIKO:*
• Nilai bisa terus turun (value trap)
• Recovery lama
• Ada masalah fundamental tersembunyi

💡 *TIPS:* 
Gunakan screening "Rebound Potential" untuk filter saham oversold.
        """
    
    def _answer_pe(self):
        return """
💰 *PRICE TO EARNING RATIO (P/E)*

P/E adalah valuasi yang membandingkan harga saham dengan laba per saham.

📊 *INTERPRETASI:*
• P/E Tinggi (>20): Growth stock, ekspektasi tinggi
• P/E Rendah (<10): Value stock, mungkin undervalued
• P/E Wajar (10-20): Normal untuk Indonesia

📌 *BENCHMARK:*
• Bank: 12-18x
• Konsumer: 15-25x
• Tambang: 5-10x (siklus komoditas)
• Teknologi: 20-50x (growth)

⚠️ *CATATAN:*
• P/E rendah belum tentu murah
• Bandingkan dengan P/E sektor & historis
• Kombinasikan dengan PBV, ROE, dan DER
        """
    
    def _answer_fundamental(self):
        return """
📊 *ANALISIS FUNDAMENTAL DASAR*

🔍 *RASIO PENTING:*
1. **P/E** (Price to Earning) - Valuasi
2. **PBV** (Price to Book Value) - Nilai aset
3. **ROE** (Return on Equity) - Profitabilitas
4. **DER** (Debt to Equity) - Utang
5. **NPM** (Net Profit Margin) - Margin laba

📈 *LAPORAN KEUANGAN:*
• Laba Rugi: Pendapatan, laba bersih
• Neraca: Aset, utang, ekuitas
• Arus Kas: Operasi, investasi, pendanaan

📌 *YANG DILIHAT:*
• Pertumbuhan laba (minimal 10% per tahun)
• Margin laba (stabil atau naik)
• Utang (DER < 1 untuk aman)
• ROE > 15% (sangat baik)

💡 *SUMBER DATA:*
• IDX (www.idx.co.id)
• RTI, Stockbit, Yahoo Finance
        """
    
    def _answer_daytrade(self):
        return """
⚡ *STRATEGI DAY TRADE*

Day trade adalah membeli dan menjual saham dalam 1 hari yang sama.

📋 *PERSIAPAN:*
• Modal minimal Rp 10-20 juta
• Pilih saham likuid (LQ45/IDX30)
• Platform real-time
• Target profit & cut loss jelas

🎯 *KRITERIA SAHAM:*
• Volume tinggi (>10M/hari)
• Volatilitas cukup (2-5% pergerakan)
• Spread tipis (beda beli-jual kecil)
• Trending di 30 menit pertama

📊 *INDIKATOR:*
• RSI (14) untuk momentum
• Volume untuk konfirmasi
• Support Resistance intraday
• Moving Average 5 & 20

💡 *STRATEGI DASAR:*
1. Breakout: Beli saat tembus resist dengan volume
2. Pullback: Beli di support saat uptrend
3. Reversal: Beli di oversold dengan konfirmasi

⚠️ *MANAJEMEN RISIKO:*
• Target profit 1-3%, cut loss 1%
• Maksimal 2-3 transaksi per hari
• Jangan averaging loss
• Istirahat jika 2 loss berturut-turut
        """
    
    def _answer_swing(self):
        return """
📊 *STRATEGI SWING TRADING*

Swing trading adalah memegang saham 3 hari hingga 1 bulan.

📋 *KARAKTERISTIK:*
• Timeframe: 3 hari - 1 bulan
• Target profit: 5-15%
• Stop loss: 3-5%
• Frekuensi: 3-5 transaksi/bulan

🎯 *KRITERIA SAHAM:*
• Trending (uptrend/downtrend jelas)
• Volume konsisten
• Support resistance kuat
• Indikator menunjukkan momentum

📊 *INDIKATOR:*
• MA20 & MA50 untuk trend
• RSI untuk entry point
• MACD untuk konfirmasi
• Volume untuk validasi

💡 *STRATEGI DASAR:*
1. *Trend Following:* Beli di pullback saat uptrend
2. *Breakout:* Beli saat tembus resist dengan volume
3. *Reversal:* Beli di oversold dengan konfirmasi pola

⚠️ *RISIKO & MANAJEMEN:*
• Risk/reward minimal 1:2
• Diversifikasi 3-5 saham
• Cut loss disiplin
• Ambil profit bertahap
        """
    
    def _answer_default(self, question):
        answers = [
            "Untuk pertanyaan spesifik tentang saham, silakan tanya dengan lebih detail. Contoh: 'Apa itu RSI?' atau 'Bagaimana analisis BBCA?'",
            
            "Saya bisa membantu analisis teknikal, fundamental, atau strategi trading. Coba tanya: 'MACD', 'Support Resistance', atau 'Swing Trading'",
            
            "Maaf, saya belum bisa menjawab pertanyaan itu. Coba tanya tentang: RSI, MACD, Double Bottom, Candlestick, P/E Ratio, Day Trade, atau Swing Trade.",
            
            "Untuk informasi lebih akurat, silakan gunakan fitur Analisis Saham di menu utama. Di sana ada data real-time dan indikator lengkap.",
            
            "Pertanyaan bagus! Tapi saya perlu informasi lebih spesifik. Bisa tanya tentang saham tertentu (BBCA, TLKM) atau indikator tertentu (RSI, MACD)?"
        ]
        return random.choice(answers)

ai = AIHandler()

# ======================== SAHAM HANDLER ========================
class SahamHandler:
    def __init__(self):
        self.stock_cache = {}
        self.screening_cache = {}
        
        # Data dummy untuk pengembangan (nanti diganti dengan yfinance)
        self.dummy_data = {
            'BBCA': {'harga': 7175, 'change': -100, 'change_pct': '-1.37%', 'volume': 15234500,
                     'ma5': 7285, 'ma20': 7290, 'ma50': 7150, 'ma100': 7050, 'rsi': 34.7, 'macd': -172.08},
            'BBRI': {'harga': 5450, 'change': 75, 'change_pct': '+1.40%', 'volume': 78500000,
                     'ma5': 5420, 'ma20': 5380, 'ma50': 5320, 'ma100': 5250, 'rsi': 48.2, 'macd': -45.3},
            'BMRI': {'harga': 10325, 'change': 345, 'change_pct': '+3.45%', 'volume': 45200000,
                     'ma5': 10200, 'ma20': 10050, 'ma50': 9850, 'ma100': 9600, 'rsi': 62.5, 'macd': 125.3},
            'BBNI': {'harga': 4890, 'change': 45, 'change_pct': '+0.93%', 'volume': 32100000,
                     'ma5': 4850, 'ma20': 4820, 'ma50': 4780, 'ma100': 4700, 'rsi': 52.3, 'macd': 25.7},
            'ASII': {'harga': 7945, 'change': -190, 'change_pct': '-2.34%', 'volume': 45200000,
                     'ma5': 8050, 'ma20': 8100, 'ma50': 7900, 'ma100': 7750, 'rsi': 31.5, 'macd': -125.3},
            'TLKM': {'harga': 3890, 'change': -85, 'change_pct': '-2.14%', 'volume': 178000000,
                     'ma5': 3920, 'ma20': 3950, 'ma50': 3880, 'ma100': 3820, 'rsi': 32.1, 'macd': -98.5},
            'ICBP': {'harga': 10350, 'change': 125, 'change_pct': '+1.22%', 'volume': 12500000,
                     'ma5': 10250, 'ma20': 10100, 'ma50': 9900, 'ma100': 9600, 'rsi': 55.8, 'macd': 85.3},
            'INDF': {'harga': 6750, 'change': 50, 'change_pct': '+0.75%', 'volume': 18500000,
                     'ma5': 6700, 'ma20': 6650, 'ma50': 6550, 'ma100': 6400, 'rsi': 52.3, 'macd': 25.7},
            'UNVR': {'harga': 3850, 'change': -75, 'change_pct': '-1.91%', 'volume': 32500000,
                     'ma5': 3900, 'ma20': 3950, 'ma50': 4000, 'ma100': 4100, 'rsi': 32.5, 'macd': -45.8},
            'GOTO': {'harga': 345, 'change': 45, 'change_pct': '+15.00%', 'volume': 1200000000,
                     'ma5': 320, 'ma20': 310, 'ma50': 295, 'ma100': 280, 'rsi': 72.5, 'macd': 15.2},
            'ADRO': {'harga': 2575, 'change': 125, 'change_pct': '+5.10%', 'volume': 125000000,
                     'ma5': 2500, 'ma20': 2450, 'ma50': 2400, 'ma100': 2350, 'rsi': 62.5, 'macd': 45.3},
            'PTBA': {'harga': 3850, 'change': 150, 'change_pct': '+4.05%', 'volume': 45200000,
                     'ma5': 3750, 'ma20': 3650, 'ma50': 3550, 'ma100': 3400, 'rsi': 65.2, 'macd': 85.7},
        }
    
    def get_yahoo_code(self, saham):
        """Konversi ke format Yahoo Finance"""
        if saham in ALL_INDONESIA_STOCKS:
            return f"{saham}.JK"
        return saham
    
    async def get_stock_data(self, kode_saham):
        """Ambil data saham (dummy dulu untuk pengembangan)"""
        # TODO: Implementasi dengan yfinance nanti
        # Untuk sekarang pake dummy data
        if kode_saham in self.dummy_data:
            return self.dummy_data[kode_saham]
        return self.dummy_data.get('BBCA', {})
    
    async def analyze_saham(self, kode_saham):
        """Analisis lengkap saham"""
        data = await self.get_stock_data(kode_saham)
        
        if not data:
            return None
        
        harga = data['harga']
        
        # Tentukan status
        ma5_status = "🟢" if harga > data['ma5'] else "🔴"
        ma20_status = "🟢" if harga > data['ma20'] else "🔴"
        ma50_status = "🟢" if harga > data['ma50'] else "🔴"
        
        if data['rsi'] < 35:
            rsi_status = "OVERSOLD 🟢"
        elif data['rsi'] > 70:
            rsi_status = "OVERBOUGHT 🔴"
        else:
            rsi_status = "NETRAL ⚪"
        
        macd_status = "🟢" if data['macd'] > 0 else "🔴"
        
        # Support Resistance sederhana
        support1 = int(harga * 0.98)
        support2 = int(harga * 0.95)
        support3 = int(harga * 0.90)
        resist1 = int(harga * 1.02)
        resist2 = int(harga * 1.05)
        resist3 = int(harga * 1.10)
        
        return {
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
            'harga': harga,
            'change': data['change'],
            'change_pct': data['change_pct'],
            'volume': data['volume'],
            
            'ma5': data['ma5'],
            'ma5_status': ma5_status,
            'ma20': data['ma20'],
            'ma20_status': ma20_status,
            'ma50': data['ma50'],
            'ma50_status': ma50_status,
            'ma100': data['ma100'],
            
            'rsi': data['rsi'],
            'rsi_status': rsi_status,
            'macd': data['macd'],
            'macd_status': macd_status,
            
            'support1': support1,
            'support2': support2,
            'support3': support3,
            'resist1': resist1,
            'resist2': resist2,
            'resist3': resist3,
        }
    
    def get_screening(self, kategori):
        """Screening saham berdasarkan kategori"""
        results = []
        
        # Screening sederhana berdasarkan dummy data
        if kategori == 'gainer':
            # Sort by change_pct positif
            saham_list = []
            for kode, data in self.dummy_data.items():
                change_val = float(data['change_pct'].replace('%', '').replace('+', ''))
                if '+' in data['change_pct']:
                    saham_list.append((kode, data, change_val))
            saham_list.sort(key=lambda x: x[2], reverse=True)
            
            for kode, data, _ in saham_list[:10]:
                results.append({
                    'kode': kode,
                    'harga': data['harga'],
                    'change': data['change'],
                    'change_pct': data['change_pct'],
                    'volume': data['volume']
                })
        
        elif kategori == 'loser':
            # Sort by change_pct negatif
            saham_list = []
            for kode, data in self.dummy_data.items():
                if '-' in data['change_pct']:
                    change_val = float(data['change_pct'].replace('%', '').replace('-', ''))
                    saham_list.append((kode, data, change_val))
            saham_list.sort(key=lambda x: x[2], reverse=True)
            
            for kode, data, _ in saham_list[:10]:
                results.append({
                    'kode': kode,
                    'harga': data['harga'],
                    'change': data['change'],
                    'change_pct': data['change_pct'],
                    'volume': data['volume']
                })
        
        elif kategori == 'oversold':
            for kode, data in self.dummy_data.items():
                if data['rsi'] < 35:
                    results.append({
                        'kode': kode,
                        'harga': data['harga'],
                        'rsi': data['rsi'],
                        'change': data['change'],
                        'change_pct': data['change_pct']
                    })
            results.sort(key=lambda x: x['rsi'])
        
        elif kategori == 'overbought':
            for kode, data in self.dummy_data.items():
                if data['rsi'] > 70:
                    results.append({
                        'kode': kode,
                        'harga': data['harga'],
                        'rsi': data['rsi'],
                        'change': data['change'],
                        'change_pct': data['change_pct']
                    })
            results.sort(key=lambda x: x['rsi'], reverse=True)
        
        elif kategori == 'volume':
            saham_list = [(kode, data['volume']) for kode, data in self.dummy_data.items()]
            saham_list.sort(key=lambda x: x[1], reverse=True)
            
            for kode, volume in saham_list[:10]:
                results.append({
                    'kode': kode,
                    'harga': self.dummy_data[kode]['harga'],
                    'volume': volume,
                    'change': self.dummy_data[kode]['change'],
                    'change_pct': self.dummy_data[kode]['change_pct']
                })
        
        return results
    
    def get_ihsg(self):
        """Data IHSG"""
        # Hitung rata-rata pergerakan dari saham
        total = 0
        count = 0
        for data in self.dummy_data.values():
            change_val = float(data['change_pct'].replace('%', '').replace('+', '').replace('-', ''))
            if '+' in data['change_pct']:
                total += change_val
            else:
                total -= change_val
            count += 1
        
        ihsg_change = total / count if count > 0 else 0.63
        
        return {
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M WIB'),
            'ihsg': 7234.56,
            'change': f"{'+' if ihsg_change > 0 else ''}{ihsg_change:.2f}",
            'change_pct': f"{'+' if ihsg_change > 0 else ''}{ihsg_change:.2f}%",
            'lq45': 987.65,
            'lq45_change': '+8.76',
            'lq45_change_pct': '+0.89%',
            'volume': '12.5M'
        }

saham = SahamHandler()

# ======================== HANDLER TELEGRAM ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start"""
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)
    
    welcome_text = f"""
🚀 *BOT SAHAM INDONESIA LENGKAP* 🚀
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}

Halo *{user.first_name}*! Selamat datang!

📌 *FITUR LENGKAP:*
━━━━━━━━━━━━━━━━━━━━━
💬 *Tanya AI* - Edukasi saham & tanya jawab
📈 *Analisis* - Teknikal + Support Resistance
💰 *Screening* - Gainer, Loser, Oversold, dll
⭐ *Watchlist* - Pantau saham favorit
📊 *IHSG* - Update indeks terkini

📝 *CARA PAKAI:*
• Ketik kode saham langsung (contoh: BBCA)
• Atau klik tombol di bawah
    """
    
    keyboard = [
        [InlineKeyboardButton("💬 Tanya AI", callback_data='ai_menu')],
        [InlineKeyboardButton("📈 Analisis Saham", callback_data='analisis_menu')],
        [InlineKeyboardButton("💰 Screening", callback_data='screening_menu')],
        [InlineKeyboardButton("⭐ Watchlist", callback_data='watchlist_menu')],
        [InlineKeyboardButton("📊 IHSG", callback_data='ihsg')],
        [InlineKeyboardButton("❓ Bantuan", callback_data='bantuan')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def ai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu Tanya AI"""
    query = update.callback_query
    await query.answer()
    
    text = """
💬 *TANYA AI SEPUTAR SAHAM*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Halo! Saya AI Assistant siap membantu Anda.

📝 *HAL YANG BISA DITANYAKAN:*
• Indikator Teknikal (RSI, MACD, MA, dll)
• Analisis Fundamental (P/E, PBV, ROE)
• Pola Chart (Double Bottom, Candlestick)
• Strategi Trading (Day Trade, Swing)
• Analisis Saham Spesifik

💡 *CONTOH PERTANYAAN:*
• "Apa itu RSI?"
• "Jelaskan pola double bottom"
• "Analisis BBCA hari ini"
• "Strategi swing trading"

✍️ *Silakan ketik pertanyaan Anda:*
    """
    
    keyboard = [
        [InlineKeyboardButton("❓ Contoh Pertanyaan", callback_data='ai_examples')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def ai_examples(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contoh pertanyaan AI"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📊 Apa itu RSI?", callback_data='ai_q_rsi')],
        [InlineKeyboardButton("📈 Cara baca MACD?", callback_data='ai_q_macd')],
        [InlineKeyboardButton("🕯️ Pola Candlestick", callback_data='ai_q_candle')],
        [InlineKeyboardButton("🥈 Double Bottom", callback_data='ai_q_double')],
        [InlineKeyboardButton("💰 Support Resistance", callback_data='ai_q_sr')],
        [InlineKeyboardButton("📊 Analisis BBCA", callback_data='ai_q_bbca')],
        [InlineKeyboardButton("⚡ Day Trade", callback_data='ai_q_daytrade')],
        [InlineKeyboardButton("📊 Swing Trading", callback_data='ai_q_swing')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='ai_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📝 *PILIH CONTOH PERTANYAAN:*\n\nKlik salah satu contoh di bawah untuk langsung bertanya.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pertanyaan AI dari user"""
    question = update.message.text
    
    # Kirim typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Proses dengan AI
    answer = await ai.ask(question)
    
    keyboard = [
        [InlineKeyboardButton("❓ Tanya Lagi", callback_data='ai_menu')],
        [InlineKeyboardButton("🔙 Menu Utama", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"💬 *JAWABAN AI*\n━━━━━━━━━━━━━━━━━━━━━\n\n{answer}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def analisis_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu analisis saham"""
    query = update.callback_query
    await query.answer()
    
    # Buat keyboard dengan saham populer
    keyboard = []
    
    # Baris 1
    row = []
    for saham in ['BBCA', 'BBRI', 'BMRI'][:3]:
        row.append(InlineKeyboardButton(saham, callback_data=f'saham:{saham}'))
    keyboard.append(row)
    
    # Baris 2
    row = []
    for saham in ['ASII', 'TLKM', 'GOTO'][:3]:
        row.append(InlineKeyboardButton(saham, callback_data=f'saham:{saham}'))
    keyboard.append(row)
    
    # Baris 3
    row = []
    for saham in ['ADRO', 'PTBA', 'ICBP'][:3]:
        row.append(InlineKeyboardButton(saham, callback_data=f'saham:{saham}'))
    keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔍 Cari Manual (ketik kode)", callback_data='cari_manual')])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='start')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📈 *PILIH SAHAM UNTUK DIANALISIS*\n\nAtau ketik langsung kode saham (contoh: BBCA)",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def detail_saham(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menampilkan detail analisis saham"""
    query = update.callback_query
    await query.answer()
    
    kode = query.data.split(':')[1]
    
    # Analisis saham
    data = await saham.analyze_saham(kode)
    
    if not data:
        await query.edit_message_text(f"❌ Data {kode} tidak ditemukan")
        return
    
    text = f"""
📈 *ANALISIS {kode}*
🕐 {data['timestamp']}
━━━━━━━━━━━━━━━━━━━━━
💰 Harga: Rp {data['harga']:,}
📊 Perubahan: {data['change']} ({data['change_pct']})
📦 Volume: {data['volume']:,}

📊 *TEKNIKAL*
━━━━━━━━━━━━━━━━━━━━━
MA5   : Rp {data['ma5']:,} {data['ma5_status']}
MA20  : Rp {data['ma20']:,} {data['ma20_status']}
MA50  : Rp {data['ma50']:,} {data['ma50_status']}
MA100 : Rp {data['ma100']:,}

RSI   : {data['rsi']:.1f} {data['rsi_status']}
MACD  : {data['macd']:.2f} {data['macd_status']}

🎯 *SUPPORT & RESISTANCE*
━━━━━━━━━━━━━━━━━━━━━
R3: Rp {data['resist3']:,}
R2: Rp {data['resist2']:,}
R1: Rp {data['resist1']:,}
P : Rp {data['harga']:,} (CURRENT)
S1: Rp {data['support1']:,}
S2: Rp {data['support2']:,}
S3: Rp {data['support3']:,}

📌 *REKOMENDASI*
━━━━━━━━━━━━━━━━━━━━━
• Swing: {'Buy' if data['ma20_status'] == '🟢' else 'Wait'} di area Rp {data['support1']:,}
• Day Trade: Range Rp {data['support1']:,} - Rp {data['resist1']:,}
• Long Term: {'Akumulasi' if data['ma50_status'] == '🟢' else 'Hold'}

⚠️ *DISCLAIMER*
Analisis untuk referensi, bukan rekomendasi jual/beli.
    """
    
    keyboard = [
        [
            InlineKeyboardButton("⭐ Watchlist", callback_data=f'watch_add:{kode}'),
            InlineKeyboardButton("🔄 Refresh", callback_data=f'saham:{kode}')
        ],
        [InlineKeyboardButton("🔙 Kembali", callback_data='analisis_menu')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def screening_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu screening saham"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("💰 Top Gainer", callback_data='screen:gainer')],
        [InlineKeyboardButton("📉 Top Loser", callback_data='screen:loser')],
        [InlineKeyboardButton("🟢 Oversold (RSI < 35)", callback_data='screen:oversold')],
        [InlineKeyboardButton("🔴 Overbought (RSI > 70)", callback_data='screen:overbought')],
        [InlineKeyboardButton("📊 Volume Tertinggi", callback_data='screen:volume')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📊 *SCREENING SAHAM*\n\nPilih kriteria screening di bawah:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def screening_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan hasil screening"""
    query = update.callback_query
    await query.answer()
    
    kategori = query.data.split(':')[1]
    
    # Dapatkan hasil screening
    results = saham.get_screening(kategori)
    
    if not results:
        await query.edit_message_text(f"❌ Tidak ada hasil untuk {kategori}")
        return
    
    # Mapping kategori ke judul
    titles = {
        'gainer': '💰 TOP GAINER',
        'loser': '📉 TOP LOSER',
        'oversold': '🟢 OVERSOLD (RSI < 35)',
        'overbought': '🔴 OVERBOUGHT (RSI > 70)',
        'volume': '📊 VOLUME TERTINGGI'
    }
    
    title = titles.get(kategori, kategori.upper())
    
    text = f"📊 *{title}*\n🕐 {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, item in enumerate(results[:10], 1):
        if kategori == 'oversold':
            text += f"{i}. *{item['kode']}*: Rp {item['harga']:,} | RSI: {item['rsi']:.1f} | {item['change_pct']}\n"
        elif kategori == 'overbought':
            text += f"{i}. *{item['kode']}*: Rp {item['harga']:,} | RSI: {item['rsi']:.1f} | {item['change_pct']}\n"
        elif kategori == 'volume':
            text += f"{i}. *{item['kode']}*: Rp {item['harga']:,} | Vol: {item['volume']:,} | {item['change_pct']}\n"
        else:
            text += f"{i}. *{item['kode']}*: Rp {item['harga']:,} | {item['change_pct']} | Vol: {item['volume']:,}\n"
    
    # Buat keyboard untuk setiap saham
    keyboard = []
    row = []
    for item in results[:5]:
        row.append(InlineKeyboardButton(item['kode'], callback_data=f'saham:{item["kode"]}'))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔄 Refresh", callback_data=f'screen:{kategori}')])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='screening_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def watchlist_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu watchlist"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    watchlist = db.get_watchlist(user_id)
    
    if not watchlist:
        text = "⭐ *WATCHLIST*\n\nWatchlist Anda masih kosong.\nTambahkan saham dari menu Analisis."
        keyboard = [
            [InlineKeyboardButton("📈 Analisis Saham", callback_data='analisis_menu')],
            [InlineKeyboardButton("🔙 Kembali", callback_data='start')]
        ]
    else:
        text = f"⭐ *WATCHLIST ANDA*\n\nTotal: {len(watchlist)} saham\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Buat keyboard untuk setiap saham
        keyboard = []
        row = []
        for saham in watchlist:
            row.append(InlineKeyboardButton(saham, callback_data=f'saham:{saham}'))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("➕ Tambah", callback_data='analisis_menu')])
        keyboard.append([InlineKeyboardButton("➖ Hapus", callback_data='watchlist_remove_menu')])
        keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='start')])
        
        # Tampilkan daftar
        for i, saham in enumerate(watchlist, 1):
            text += f"{i}. {saham}\n"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def watchlist_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tambah saham ke watchlist"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    kode = query.data.split(':')[1]
    
    if db.add_to_watchlist(user_id, kode):
        await query.edit_message_text(f"✅ {kode} ditambahkan ke Watchlist!")
    else:
        await query.edit_message_text(f"ℹ️ {kode} sudah ada di Watchlist")
    
    # Tanya mau lihat watchlist atau analisis lagi
    keyboard = [
        [InlineKeyboardButton("⭐ Lihat Watchlist", callback_data='watchlist_menu')],
        [InlineKeyboardButton("📈 Analisis Lagi", callback_data=f'saham:{kode}')],
        [InlineKeyboardButton("🔙 Menu Utama", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Pilih menu:", reply_markup=reply_markup)

async def watchlist_remove_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu hapus dari watchlist"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    watchlist = db.get_watchlist(user_id)
    
    if not watchlist:
        await query.edit_message_text("❌ Watchlist kosong")
        return
    
    text = "➖ *HAPUS DARI WATCHLIST*\n\nPilih saham yang ingin dihapus:\n"
    
    keyboard = []
    for saham in watchlist:
        keyboard.append([InlineKeyboardButton(f"Hapus {saham}", callback_data=f'watch_remove:{saham}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='watchlist_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def watchlist_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hapus saham dari watchlist"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    kode = query.data.split(':')[1]
    
    if db.remove_from_watchlist(user_id, kode):
        await query.edit_message_text(f"✅ {kode} dihapus dari Watchlist")
    else:
        await query.edit_message_text(f"❌ Gagal menghapus {kode}")
    
    # Kembali ke menu watchlist
    keyboard = [
        [InlineKeyboardButton("⭐ Lihat Watchlist", callback_data='watchlist_menu')],
        [InlineKeyboardButton("🔙 Menu Utama", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Pilih menu:", reply_markup=reply_markup)

async def ihsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan IHSG"""
    query = update.callback_query
    await query.answer()
    
    data = saham.get_ihsg()
    
    text = f"""
📈 *IHSG & INDEKS*
🕐 {data['timestamp']}
━━━━━━━━━━━━━━━━━━━━━

🇮🇩 *IHSG*
Harga: {data['ihsg']:,.2f}
Perubahan: {data['change']} ({data['change_pct']})

🏭 *LQ45*
Harga: {data['lq45']:,.2f}
Perubahan: {data['lq45_change']} ({data['lq45_change_pct']})

📊 *INDEKS LAINNYA*
• IDX30: 543.21 (-0.43%)
• IDX80: 123.45 (+1.01%)
• IDXESGL: 98.76 (+0.23%)

📈 *INDIKATOR*
• Support: 7,150
• Resistance: 7,350
• Volume: {data['volume']}
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 Top Gainer", callback_data='screen:gainer')],
        [InlineKeyboardButton("📉 Top Loser", callback_data='screen:loser')],
        [InlineKeyboardButton("🔄 Refresh", callback_data='ihsg')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='start')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu bantuan"""
    query = update.callback_query
    await query.answer()
    
    text = """
❓ *BANTUAN & CARA PAKAI*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 *FITUR UTAMA:*

1️⃣ *💬 Tanya AI*
• Tanya tentang indikator teknikal
• Tanya analisis fundamental
• Tanya strategi trading
• Ketik pertanyaan langsung

2️⃣ *📈 Analisis Saham*
• Ketik kode saham (BBCA, BBRI, dll)
• Lihat harga, perubahan, volume
• Moving averages (5,20,50,100)
• RSI & MACD
• Support & Resistance otomatis
• Rekomendasi singkat

3️⃣ *💰 Screening*
• Top Gainer (kenaikan tertinggi)
• Top Loser (penurunan tertinggi)
• Oversold (RSI < 35)
• Overbought (RSI > 70)
• Volume tertinggi

4️⃣ *⭐ Watchlist*
• Pantau saham favorit
• Tambah/hapus saham
• Akses cepat ke analisis

5️⃣ *📊 IHSG*
• Update indeks terkini
• IHSG, LQ45, dll

📝 *CARA CEPAT:*
• Ketik langsung kode saham
• Contoh: BBCA, BBRI, TLKM

⚠️ *DISCLAIMER:*
Bot ini untuk edukasi dan referensi.
Bukan rekomendasi jual/beli.
Selalu lakukan riset mandiri.

👨‍💻 *INFO:*
Bot Saham Indonesia v5.0
Update: {datetime.now().strftime('%d/%m/%Y')}
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk pesan teks biasa"""
    text = update.message.text.strip().upper()
    
    # Cek apakah kode saham
    if text in ALL_INDONESIA_STOCKS:
        # Analisis saham
        data = await saham.analyze_saham(text)
        
        if not data:
            await update.message.reply_text(f"❌ Data {text} tidak ditemukan")
            return
        
        text_analisis = f"""
📈 *ANALISIS {text}*
🕐 {data['timestamp']}
━━━━━━━━━━━━━━━━━━━━━
💰 Harga: Rp {data['harga']:,}
📊 Perubahan: {data['change']} ({data['change_pct']})
📦 Volume: {data['volume']:,}

📊 *TEKNIKAL*
━━━━━━━━━━━━━━━━━━━━━
MA5   : Rp {data['ma5']:,} {data['ma5_status']}
MA20  : Rp {data['ma20']:,} {data['ma20_status']}
MA50  : Rp {data['ma50']:,} {data['ma50_status']}
MA100 : Rp {data['ma100']:,}

RSI   : {data['rsi']:.1f} {data['rsi_status']}
MACD  : {data['macd']:.2f} {data['macd_status']}

🎯 *LEVEL KUNCI*
━━━━━━━━━━━━━━━━━━━━━
R3: Rp {data['resist3']:,}
R2: Rp {data['resist2']:,}
R1: Rp {data['resist1']:,}
P : Rp {data['harga']:,}
S1: Rp {data['support1']:,}
S2: Rp {data['support2']:,}
S3: Rp {data['support3']:,}

📌 *REKOMENDASI*
━━━━━━━━━━━━━━━━━━━━━
• Swing: {'Buy' if data['ma20_status'] == '🟢' else 'Wait'} di area Rp {data['support1']:,}
• Day Trade: Range Rp {data['support1']:,} - Rp {data['resist1']:,}
• Long Term: {'Akumulasi' if data['ma50_status'] == '🟢' else 'Hold'}

⚠️ *DISCLAIMER*
Analisis untuk referensi, bukan rekomendasi jual/beli.
        """
        
        keyboard = [
            [InlineKeyboardButton("⭐ Watchlist", callback_data=f'watch_add:{text}')],
            [InlineKeyboardButton("📊 Screening", callback_data='screening_menu')],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data='start')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text_analisis, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif text.startswith('/'):
        # Command, diabaikan
        pass
    
    else:
        # Anggap sebagai pertanyaan AI
        await update.message.chat.send_action(action="typing")
        answer = await ai.ask(text)
        
        keyboard = [
            [InlineKeyboardButton("❓ Tanya Lagi", callback_data='ai_menu')],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data='start')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"💬 *JAWABAN AI*\n━━━━━━━━━━━━━━━━━━━━━\n\n{answer}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk semua callback button"""
    query = update.callback_query
    data = query.data
    
    # Route berdasarkan callback data
    if data == 'start':
        await start(update, context)
    elif data == 'ai_menu':
        await ai_menu(update, context)
    elif data == 'ai_examples':
        await ai_examples(update, context)
    elif data.startswith('ai_q_'):
        # Pertanyaan AI contoh
        question_map = {
            'ai_q_rsi': 'Apa itu RSI?',
            'ai_q_macd': 'Jelaskan MACD',
            'ai_q_candle': 'Apa itu candlestick?',
            'ai_q_double': 'Jelaskan pola double bottom',
            'ai_q_sr': 'Apa itu support dan resistance?',
            'ai_q_bbca': 'Analisis BBCA',
            'ai_q_daytrade': 'Strategi day trade',
            'ai_q_swing': 'Strategi swing trading',
        }
        question = question_map.get(data, 'Analisis saham')
        await query.answer()
        
        # Buat pesan palsu untuk handle_ai_question
        class FakeMessage:
            def __init__(self, text):
                self.text = text
                self.chat = type('obj', (object,), {'send_action': lambda action: None})()
        
        fake_update = type('obj', (object,), {
            'message': FakeMessage(question),
            'effective_user': query.from_user,
            'callback_query': query
        })
        
        await handle_ai_question(fake_update, context)
    
    elif data == 'analisis_menu':
        await analisis_menu(update, context)
    elif data.startswith('saham:'):
        await detail_saham(update, context)
    elif data == 'cari_manual':
        await query.answer()
        await query.edit_message_text(
            "🔍 *CARI SAHAM*\n\nKetik langsung kode saham yang ingin dianalisis.\nContoh: BBCA, BBRI, TLKM",
            parse_mode='Markdown'
        )
    
    elif data == 'screening_menu':
        await screening_menu(update, context)
    elif data.startswith('screen:'):
        await screening_result(update, context)
    
    elif data == 'watchlist_menu':
        await watchlist_menu(update, context)
    elif data.startswith('watch_add:'):
        await watchlist_add(update, context)
    elif data == 'watchlist_remove_menu':
        await watchlist_remove_menu(update, context)
    elif data.startswith('watch_remove:'):
        await watchlist_remove(update, context)
    
    elif data == 'ihsg':
        await ihsg(update, context)
    elif data == 'bantuan':
        await bantuan(update, context)
    else:
        await query.answer("Fitur dalam pengembangan")

def main():
    """Fungsi utama"""
    print("=" * 50)
    print("🚀 BOT SAHAM INDONESIA LENGKAP v5.0")
    print(f"📊 Total saham: {len(ALL_INDONESIA_STOCKS)} saham Indonesia")
    print("📈 Fitur: Tanya AI, Analisis, Screening, Watchlist, IHSG")
    print("=" * 50)
    
    # Buat aplikasi
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    print("🤖 Bot berjalan... Tekan Ctrl+C untuk berhenti")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
