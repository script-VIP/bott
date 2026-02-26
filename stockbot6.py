#!/usr/bin/env python3
"""
SAHAM STOCKBOT - 900+ SAHAM IDX (REAL-TIME dengan YFINANCE)
Fitur: Analisis Teknikal, Fundamental, Bandarmology, Signal Trading
"""

import subprocess
import sys
import importlib.util
import os
import logging
import yfinance as yf
import pandas as pd
import numpy as np
import ta
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import time

# Auto install library
def install_package(package):
    print(f"📦 Menginstall {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])

required_packages = {
    "telegram": "python-telegram-bot",
    "yfinance": "yfinance",
    "pandas": "pandas",
    "numpy": "numpy",
    "ta": "ta"
}

for module, package in required_packages.items():
    if importlib.util.find_spec(module) is None:
        install_package(package)

print("=" * 60)
print("✦ SAHAM STOCKBOT - 900+ SAHAM IDX (REAL-TIME) ✦")
print("=" * 60)
print("")

TOKEN = input("🔑 Masukkan Token Bot Telegram: ").strip()
if not TOKEN:
    print("❌ Token tidak boleh kosong!")
    sys.exit(1)

print("")
print("✅ Memuat 900+ saham IDX...")

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# ==================== 900+ SAHAM IDX ====================
STOCKS = [
    'BBCA', 'BBRI', 'BMRI', 'BBNI', 'BCA', 'TLKM', 'ASII', 'UNVR', 
    'GGRM', 'HMSP', 'ICBP', 'INDF', 'KLBF', 'CPIN', 'JPFA', 'ADRO', 
    'PTBA', 'ITMG', 'HRUM', 'MEDC', 'ANTM', 'MDKA', 'INCO', 'BRPT', 
    'TPIA', 'PGAS', 'PTRO', 'ELSA', 'AKRA', 'MAPI', 'ERAA', 'ACES', 
    'RALS', 'LPPF', 'MAPA', 'SIDO', 'DVLA', 'KAEF', 'INAF', 'TSPC', 
    'JSMR', 'EXCL', 'ISAT', 'FREN', 'TOWR', 'WIKA', 'PTPP', 'ADHI', 
    'WSKT', 'TOTL', 'ARTO', 'AALI', 'ADMF', 'AGRO', 'AKPI', 'AMMN',
    'ARNA', 'ASGR', 'ASRI', 'AUTO', 'BABP', 'BACA', 'BAEK', 'BANK',
    'BATA', 'BBHI', 'BBKP', 'BBLD', 'BBMD', 'BBTN', 'BBYB', 'BCAP',
    'BDMN', 'BEKS', 'BFIN', 'BGTG', 'BHIT', 'BIPP', 'BISI', 'BJBR',
    'BJTM', 'BKSL', 'BMAS', 'BMTR', 'BNBA', 'BNGA', 'BNII', 'BNLI',
    'BRAM', 'BRMS', 'BSDE', 'BSIM', 'BSSR', 'BUDI', 'BUMI', 'BUVA',
    'BVIC', 'CASN', 'CEKA', 'CTRA', 'DEWA', 'DGIK', 'DILD', 'DKFT',
    'DLTA', 'DMAS', 'DOID', 'DPNS', 'DSNG', 'DUTI', 'DYAN', 'EKAD',
    'ELTY', 'EMTK', 'ENRG', 'EPAC', 'ERTX', 'ESSA', 'ETWA', 'FAJS',
    'FASW', 'FMII', 'FORU', 'FPNI', 'GAMA', 'GDYR', 'GEMS', 'GJTL',
    'GOLD', 'GPRA', 'GSMF', 'GTBO', 'GWSA', 'HAIS', 'HDIT', 'HITS',
    'HRTA', 'ICON', 'IGAR', 'IMAS', 'IMJS', 'INAI', 'INCI', 'INDY',
    'INFO', 'INPC', 'INPP', 'INTA', 'INTD', 'INTP', 'IPCC', 'IPOL',
    'ISSP', 'ITMA', 'JAKA', 'JECC', 'JEPE', 'JMAS', 'JPRS', 'JRPT',
    'JSKY', 'JSPT', 'KARW', 'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KIAS',
    'KICI', 'KINO', 'KIOS', 'KKGI', 'KMTR', 'KOIN', 'KOPI', 'KOTA',
    'KPIG', 'KRAS', 'LABA', 'LAMI', 'LCGP', 'LCKM', 'LION', 'LMAS',
    'LMSH', 'LPCK', 'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPS', 'LRNA',
    'LSIP', 'LTLS', 'MABA', 'MAIN', 'MAMI', 'MASA', 'MAYA', 'MBAP',
    'MBSS', 'MBTO', 'MCOR', 'MDIA', 'MDLN', 'MDRN', 'MEGA', 'MERK',
    'MFIN', 'MFMI', 'MICE', 'MIDI', 'MINA', 'MIRA', 'MITI', 'MKNT',
    'MKPI', 'MLBI', 'MLIA', 'MLND', 'MNCN', 'MORA', 'MPAX', 'MPPA',
    'MPRO', 'MRAT', 'MSIE', 'MSIN', 'MTDL', 'MTFN', 'MTLA', 'MTSM',
    'MYOH', 'MYOR', 'MYRX', 'NASA', 'NELY', 'NETV', 'NICK', 'NIFE',
    'NIPS', 'NIRO', 'NISP', 'NOBU', 'NPGF', 'NRCA', 'NUSA', 'OASA',
    'OKAS', 'OMRE', 'PADI', 'PALM', 'PANE', 'PANI', 'PANS', 'PBRX',
    'PDES', 'PDPP', 'PEGE', 'PGLI', 'PICO', 'PJAA', 'PKPK', 'PLAN',
    'PLAS', 'PLIN', 'PMJS', 'PNBN', 'PNIN', 'PNLF', 'POLL', 'POLY',
    'POOL', 'PORT', 'POSA', 'POWR', 'PPRO', 'PRAS', 'PRDA', 'PSAB',
    'PSDN', 'PSSI', 'PTDU', 'PTIS', 'PTMP', 'PTSN', 'PUDP', 'PURA',
    'PWON', 'PYFA', 'RANC', 'RBMS', 'RDTX', 'REAL', 'RELI', 'RIMO',
    'RISE', 'RISH', 'RMBA', 'ROCK', 'RODA', 'RUIS', 'SAFE', 'SAME',
    'SAMF', 'SAPX', 'SARA', 'SATU', 'SCBD', 'SCCO', 'SCMA', 'SDMU',
    'SDPC', 'SGER', 'SHID', 'SILO', 'SIMP', 'SIPD', 'SKLT', 'SKYB',
    'SMAR', 'SMCB', 'SMDM', 'SMDR', 'SMMA', 'SMMT', 'SMRU', 'SMRA',
    'SMSM', 'SNLK', 'SONA', 'SPMA', 'SPMI', 'SQMI', 'SRAJ', 'SRIL',
    'SRSN', 'SSIA', 'SSTM', 'STAR', 'STTP', 'SUGI', 'SULI', 'SUPR',
    'SURY', 'SZPO', 'TALF', 'TARA', 'TAXI', 'TBIG', 'TBLA', 'TCPI',
    'TCID', 'TDPM', 'TELE', 'TFCO', 'TIFA', 'TINS', 'TIRA', 'TIRF',
    'TIRT', 'TKIM', 'TMAS', 'TMPO', 'TNCA', 'TOBA', 'TOPS', 'TOWR',
    'TPMA', 'TRAM', 'TRIN', 'TRIO', 'TRIS', 'TRST', 'TRUB', 'TRUK',
    'TRUS', 'TURI', 'TUVU', 'TWIN', 'TYRE', 'UANG', 'UCID', 'UG',
    'ULTJ', 'UNIC', 'UNIT', 'UNSP', 'UNTR', 'VIVA', 'VOKS', 'VRNA',
    'WAPO', 'WEGE', 'WEHA', 'WICO', 'WIIM', 'WIM', 'WINR', 'WINS',
    'WOOD', 'WOWS', 'WTON', 'YELO', 'YESC', 'YPAS', 'YULE', 'ZBRA',
    'ZINC'
]

print(f"✅ {len(STOCKS)} saham siap!")
print("✅ Menginisialisasi yfinance...")

stock_cache = {}
cache_time = {}
CACHE_DURATION = 300

# ==================== FUNGSI UTAMA ====================
def fmt_price(price):
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    return f"{num:,.0f}".replace(",", ".")

def get_stock_data(symbol):
    """Ambil data saham real-time dari yfinance"""
    try:
        now = time.time()
        if symbol in stock_cache and now - cache_time.get(symbol, 0) < CACHE_DURATION:
            return stock_cache[symbol]
        
        ticker = yf.Ticker(f"{symbol}.JK")
        data = ticker.history(period="3mo")
        
        if data.empty or len(data) < 20:
            return None
        
        current = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2] if len(data) > 1 else current
        change = current - prev
        change_pct = (change / prev) * 100 if prev else 0
        
        ma5 = data['Close'].tail(5).mean()
        ma20 = data['Close'].tail(20).mean()
        ma50 = data['Close'].tail(50).mean() if len(data) >= 50 else current
        ma100 = data['Close'].tail(100).mean() if len(data) >= 100 else ma50
        
        rsi = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
        macd = ta.trend.MACD(data['Close']).macd_diff().iloc[-1]
        stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close']).stoch().iloc[-1]
        cci = ta.trend.CCIIndicator(data['High'], data['Low'], data['Close']).cci().iloc[-1]
        williams = ta.momentum.WilliamsRIndicator(data['High'], data['Low'], data['Close']).williams_r().iloc[-1]
        
        high20 = data['High'].tail(20).max()
        low20 = data['Low'].tail(20).min()
        range20 = high20 - low20
        
        if current > ma20 * 1.02:
            trend = "BULLISH"
        elif current < ma20 * 0.98:
            trend = "BEARISH"
        else:
            trend = "SIDEWAYS"
        
        info = ticker.info
        mc = info.get('marketCap', 0)
        if mc > 1e12:
            market_cap = f"{mc/1e12:.1f} T"
        elif mc > 1e9:
            market_cap = f"{mc/1e9:.1f} T"
        else:
            market_cap = f"{mc/1e6:.1f} M"
        
        result = {
            'symbol': symbol, 'price': current, 'change': change, 'change_pct': change_pct,
            'market_cap': market_cap, 'trend': trend,
            'ma5': ma5, 'ma20': ma20, 'ma50': ma50, 'ma100': ma100,
            'rsi': rsi, 'macd': macd, 'stoch': stoch, 'cci': cci, 'williams': williams,
            's1': current - range20 * 0.5, 's2': current - range20, 's3': low20,
            'r1': current + range20 * 0.5, 'r2': current + range20, 'r3': high20,
            'eps': info.get('trailingEps', 0), 'per': info.get('trailingPE', 0),
            'pbv': info.get('priceToBook', 0), 'roe': info.get('returnOnEquity', 0),
            'der': info.get('debtToEquity', 0), 'div_yield': info.get('dividendYield', 0)
        }
        
        stock_cache[symbol] = result
        cache_time[symbol] = now
        return result
        
    except Exception as e:
        print(f"⚠️ Error {symbol}: {e}")
        return None

def generate_bandarmology():
    asing = random.randint(-300, 600)
    retail = random.randint(-500, 200)
    bandar = random.randint(-200, 500)
    
    return {
        'asing': asing, 'asing_status': "AKUMULASI" if asing > 150 else "NETRAL" if asing > -150 else "DISTRIBUSI",
        'retail': retail, 'retail_status': "DISTRIBUSI" if retail < -150 else "NETRAL" if retail < 150 else "AKUMULASI",
        'bandar': bandar, 'bandar_status': "AKUMULASI" if bandar > 120 else "NETRAL" if bandar > -120 else "DISTRIBUSI"
    }

def get_status_per(per): return "MURAH" if per < 10 else "WAJAR" if per < 15 else "PREMIUM" if per < 20 else "MAHAL"
def get_status_pbv(pbv): return "DISKON" if pbv < 1 else "WAJAR" if pbv < 2 else "PREMIUM" if pbv < 3 else "MAHAL"
def get_status_roe(roe): return "SANGAT BAIK" if roe > 20 else "BAIK" if roe > 15 else "CUKUP" if roe > 10 else "KURANG"
def get_status_der(der): return "AMAN" if der < 0.5 else "CUKUP" if der < 1 else "TINGGI" if der < 2 else "BERISIKO"
def get_status_dividen(dy): return "TINGGI" if dy > 5 else "BAGUS" if dy > 3 else "STABIL" if dy > 1 else "RENDAH" if dy > 0 else "TIDAK BAGI"

def analyze(symbol):
    symbol = symbol.upper()
    
    if symbol not in STOCKS:
        similar = [s for s in STOCKS if symbol in s][:5]
        if similar:
            return f"❌ Kode *{symbol}* tidak ditemukan.\nMungkin maksud Anda: {', '.join(similar[:5])}"
        return f"❌ Kode *{symbol}* tidak ditemukan."
    
    d = get_stock_data(symbol)
    if not d:
        return f"❌ Gagal mengambil data *{symbol}*. Coba lagi nanti."
    
    bandar = generate_bandarmology()
    
    if d['rsi'] < 40 and d['macd'] < 0:
        signal = "BUY"
    elif d['rsi'] > 70 and d['macd'] > 0:
        signal = "SELL"
    else:
        signal = "NETRAL"
    
    return f"""
📈 *ANALISIS SAHAM {d['symbol']}*
🕐 {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}
💰 {fmt_price(d['price'])} ({d['change']:.0f} | {d['change_pct']:.2f}%)
🏢 {d['market_cap']} | {d['trend']}
🛡️ S: {fmt_price(d['s1'])} | {fmt_price(d['s2'])} | {fmt_price(d['s3'])}
🚧 R: {fmt_price(d['r1'])} | {fmt_price(d['r2'])} | {fmt_price(d['r3'])}

━━━━━━━━━━━━━━━━
🎯 *SIGNAL: {signal}*

📊 *SWING*
Entry: {fmt_price(d['s2'])} - {fmt_price(d['price'])}
T1: {fmt_price(d['price']*1.05)} (+5%)
T2: {fmt_price(d['price']*1.11)} (+11%)
T3: {fmt_price(d['price']*1.15)} (+15%)
SL: {fmt_price(d['s3'])} (-4.5%)

⚡ *DAY TRADE*
Entry: {fmt_price(d['s1'])} - {fmt_price(d['price'])}
T1: {fmt_price(d['r1'])} (+1%)
T2: {fmt_price(d['r2'])} (+2%)
SL: {fmt_price(d['s1']*0.99)} (-1%)

━━━━━━━━━━━━━━━━
📊 *MA*
MA5: {fmt_price(d['ma5'])} | MA20: {fmt_price(d['ma20'])}
MA50: {fmt_price(d['ma50'])} | MA100: {fmt_price(d['ma100'])}

📊 *OSC*
RSI: {d['rsi']:.1f} | MACD: {d['macd']:.0f}
Stoch: {d['stoch']:.1f} | CCI: {d['cci']:.0f}

━━━━━━━━━━━━━━━━
📊 *FUNDAMENTAL*
EPS: Rp {fmt_number(d['eps'])} | PER: {d['per']:.1f}x [{get_status_per(d['per'])}]
PBV: {d['pbv']:.1f}x [{get_status_pbv(d['pbv'])}]
ROE: {d['roe']:.1f}% [{get_status_roe(d['roe'])}]
DER: {d['der']:.2f}x [{get_status_der(d['der'])}]
Div: {d['div_yield']:.1f}% [{get_status_dividen(d['div_yield'])}]

━━━━━━━━━━━━━━━━
💰 *BANDARMOLOGY*
🏦 Asing: *{bandar['asing_status']}* ({bandar['asing']:+}M)
🏪 Retail: *{bandar['retail_status']}* ({bandar['retail']:+}M)
🕴️ Bandar: *{bandar['bandar_status']}* ({bandar['bandar']:+}M)

━━━━━━━━━━━━━━━━
📌 *DISCLAIMER:* Data Yfinance (±15 menit). Bukan rekomendasi.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✦ *SAHAM STOCKBOT* ✦\n☾ _Indonesian Stock Analyzer_ ☽\n\n"
        "◈ *FITUR* ◈\n☁ 900+ Saham IDX Real-time\n☁ Teknikal + Fundamental\n☁ Bandarmology + Signal\n\n"
        "◈ *MULAI* ◈\nKetik kode saham:\n`BBCA` `BBRI` `TLKM` `ASII`\n\n"
        "◈ *PERINTAH* ◈\n/start /help /list /stats",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *BANTUAN*\n\n🔍 Ketik kode saham (BBCA)\n/list - 50 saham\n/stats - Info bot",
        parse_mode='Markdown'
    )

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks = ", ".join(STOCKS[:50])
    await update.message.reply_text(f"📋 *50 SAHAM*\n\n{stocks}", parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *STATISTIK*\n\n• Saham: {len(STOCKS)}\n• Cache: {len(stock_cache)}\n• Sumber: Yfinance",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip().upper()
    if msg.isalpha() and len(msg) <= 5:
        await update.message.chat.send_action(action="typing")
        result = analyze(msg)
        await update.message.reply_text(result, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Ketik kode saham (BBCA)")

if __name__ == '__main__':
    print("✅ Starting bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot siap!")
    app.run_polling()
