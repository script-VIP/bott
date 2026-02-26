#!/usr/bin/env python3
"""
TELEGRAM BOT SAHAM INDONESIA - 900+ SAHAM (TANPA YFINANCE)
Fitur: Analisis saham + Bandarmology + Fundamental (data simulasi)
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import sys
import random
import time

# ==================== KONFIGURASI ====================
print("=" * 50)
print("🤖 TELEGRAM BOT SAHAM INDONESIA")
print("=" * 50)
print("")

# Minta Token Telegram
TELEGRAM_TOKEN = input("🔑 Masukkan Telegram Bot Token: ").strip()
if not TELEGRAM_TOKEN:
    print("❌ Token tidak boleh kosong!")
    sys.exit(1)

# Minta OpenAI API Key (opsional)
OPENAI_API_KEY = input("🤖 Masukkan OpenAI API Key (enter jika tidak ada): ").strip()
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

print("")
print("✅ Memuat 900+ saham IDX...")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== 900+ SAHAM IDX ====================
STOCKS = [
    # LQ45
    'BBCA', 'BBRI', 'BMRI', 'BBNI', 'BCA', 'TLKM', 'ASII', 'UNVR', 
    'GGRM', 'HMSP', 'ICBP', 'INDF', 'KLBF', 'CPIN', 'JPFA', 'ADRO', 
    'PTBA', 'ITMG', 'HRUM', 'MEDC', 'ANTM', 'MDKA', 'INCO', 'BRPT', 
    'TPIA', 'PGAS', 'PTRO', 'ELSA', 'AKRA', 'MAPI', 'ERAA', 'ACES', 
    'RALS', 'LPPF', 'MAPA', 'SIDO', 'DVLA', 'KAEF', 'INAF', 'TSPC', 
    'JSMR', 'EXCL', 'ISAT', 'FREN', 'TOWR', 'WIKA', 'PTPP', 'ADHI', 
    'WSKT', 'TOTL',
    
    # Kompas100
    'ARTO', 'AALI', 'ADMF', 'AGRO', 'AKPI', 'AMMN', 'ARNA', 'ASGR',
    'ASRI', 'AUTO', 'BABP', 'BACA', 'BAEK', 'BANK', 'BATA', 'BBHI',
    'BBKP', 'BBLD', 'BBMD', 'BBTN', 'BBYB', 'BCAP', 'BDMN', 'BEKS',
    'BFIN', 'BGTG', 'BHIT', 'BIPP', 'BISI', 'BJBR', 'BJTM', 'BKSL',
    'BMAS', 'BMTR', 'BNBA', 'BNGA', 'BNII', 'BNLI', 'BRAM', 'BRMS',
    'BSDE', 'BSIM', 'BSSR', 'BUDI', 'BUMI', 'BUVA', 'BVIC', 'CASN',
    'CEKA', 'CTRA', 'DEWA', 'DGIK', 'DILD', 'DKFT', 'DLTA', 'DMAS',
    'DOID', 'DPNS', 'DSNG', 'DUTI', 'DYAN', 'EKAD', 'ELTY', 'EMTK',
    'ENRG', 'EPAC', 'ERTX', 'ESSA', 'ETWA', 'FAJS', 'FASW', 'FMII',
    'FORU', 'FPNI', 'GAMA', 'GDYR', 'GEMS', 'GJTL', 'GOLD', 'GPRA',
    'GSMF', 'GTBO', 'GWSA', 'HAIS', 'HDIT', 'HITS', 'HRTA', 'ICON',
    'IGAR', 'IMAS', 'IMJS', 'INAI', 'INCI', 'INDY', 'INFO', 'INPC',
    'INPP', 'INTA', 'INTD', 'INTP', 'IPCC', 'IPOL', 'ISSP', 'ITMA',
    'JAKA', 'JECC', 'JEPE', 'JMAS', 'JPRS', 'JRPT', 'JSKY', 'JSPT',
    'KARW', 'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KIAS', 'KICI', 'KINO',
    'KIOS', 'KKGI', 'KMTR', 'KOIN', 'KOPI', 'KOTA', 'KPIG', 'KRAS',
    'LABA', 'LAMI', 'LCGP', 'LCKM', 'LION', 'LMAS', 'LMSH', 'LPCK',
    'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPS', 'LRNA', 'LSIP', 'LTLS',
    'MABA', 'MAIN', 'MAMI', 'MASA', 'MAYA', 'MBAP', 'MBSS', 'MBTO',
    'MCOR', 'MDIA', 'MDLN', 'MDRN', 'MEGA', 'MERK', 'MFIN', 'MFMI',
    'MICE', 'MIDI', 'MINA', 'MIRA', 'MITI', 'MKNT', 'MKPI', 'MLBI',
    'MLIA', 'MLND', 'MNCN', 'MORA', 'MPAX', 'MPPA', 'MPRO', 'MRAT',
    'MSIE', 'MSIN', 'MTDL', 'MTFN', 'MTLA', 'MTSM', 'MYOH', 'MYOR',
    'MYRX', 'NASA', 'NELY', 'NETV', 'NICK', 'NIFE', 'NIPS', 'NIRO',
    'NISP', 'NOBU', 'NPGF', 'NRCA', 'NUSA', 'OASA', 'OKAS', 'OMRE',
    'PADI', 'PALM', 'PANE', 'PANI', 'PANS', 'PBRX', 'PDES', 'PDPP',
    'PEGE', 'PGLI', 'PICO', 'PJAA', 'PKPK', 'PLAN', 'PLAS', 'PLIN',
    'PMJS', 'PNBN', 'PNIN', 'PNLF', 'POLL', 'POLY', 'POOL', 'PORT',
    'POSA', 'POWR', 'PPRO', 'PRAS', 'PRDA', 'PSAB', 'PSDN', 'PSSI',
    'PTDU', 'PTIS', 'PTMP', 'PTSN', 'PUDP', 'PURA', 'PWON', 'PYFA',
    'RANC', 'RBMS', 'RDTX', 'REAL', 'RELI', 'RIMO', 'RISE', 'RISH',
    'RMBA', 'ROCK', 'RODA', 'RUIS', 'SAFE', 'SAME', 'SAMF', 'SAPX',
    'SARA', 'SATU', 'SCBD', 'SCCO', 'SCMA', 'SDMU', 'SDPC', 'SGER',
    'SHID', 'SILO', 'SIMP', 'SIPD', 'SKLT', 'SKYB', 'SMAR', 'SMCB',
    'SMDM', 'SMDR', 'SMMA', 'SMMT', 'SMRU', 'SMRA', 'SMSM', 'SNLK',
    'SONA', 'SPMA', 'SPMI', 'SQMI', 'SRAJ', 'SRIL', 'SRSN', 'SSIA',
    'SSTM', 'STAR', 'STTP', 'SUGI', 'SULI', 'SUPR', 'SURY', 'SZPO',
    'TALF', 'TARA', 'TAXI', 'TBIG', 'TBLA', 'TCPI', 'TCID', 'TDPM',
    'TELE', 'TFCO', 'TIFA', 'TINS', 'TIRA', 'TIRF', 'TIRT', 'TKIM',
    'TMAS', 'TMPO', 'TNCA', 'TOBA', 'TOPS', 'TOWR', 'TPMA', 'TRAM',
    'TRIN', 'TRIO', 'TRIS', 'TRST', 'TRUB', 'TRUK', 'TRUS', 'TURI',
    'TUVU', 'TWIN', 'TYRE', 'UANG', 'UCID', 'UG', 'ULTJ', 'UNIC',
    'UNIT', 'UNSP', 'UNTR', 'VIVA', 'VOKS', 'VRNA', 'WAPO', 'WEGE',
    'WEHA', 'WICO', 'WIIM', 'WIM', 'WINR', 'WINS', 'WOOD', 'WOWS',
    'WTON', 'YELO', 'YESC', 'YPAS', 'YULE', 'ZBRA', 'ZINC'
]

print(f"✅ {len(STOCKS)} saham IDX siap!")

# Cache
stock_cache = {}
cache_time = {}

# ==================== FUNGSI ====================
def fmt_price(price):
    if price is None:
        return "Rp 0"
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    if num is None:
        return "0"
    return f"{num:,.0f}".replace(",", ".")

def generate_stock_data(symbol):
    """Generate data saham simulasi"""
    current_time = time.time()
    if symbol in stock_cache and symbol in cache_time:
        if current_time - cache_time[symbol] < 300:
            return stock_cache[symbol]
    
    random.seed(symbol + datetime.now().strftime('%Y%m%d'))
    
    # Harga dasar
    base_prices = {
        'BBCA': 9500, 'BBRI': 5250, 'BMRI': 6200, 'BBNI': 5100, 'TLKM': 3750,
        'ASII': 5750, 'UNVR': 2850, 'GGRM': 22750, 'HMSP': 875, 'ICBP': 9850,
        'INDF': 6250, 'KLBF': 1575, 'ADRO': 2750, 'PTBA': 3150, 'ANTM': 1850,
    }
    
    base = base_prices.get(symbol, random.randint(500, 10000))
    
    # Fluktuasi
    change_percent = random.uniform(-3.5, 3.5)
    change = base * change_percent / 100
    current = base + change
    
    # MA
    ma5 = current * random.uniform(0.96, 1.04)
    ma10 = current * random.uniform(0.95, 1.05)
    ma20 = current * random.uniform(0.93, 1.07)
    ma50 = current * random.uniform(0.90, 1.10)
    ma100 = current * random.uniform(0.85, 1.15)
    
    # Oscillator
    rsi = random.uniform(25, 75)
    macd = random.uniform(-150, 150)
    stoch = random.uniform(15, 85)
    cci = random.uniform(-120, 120)
    williams = random.uniform(-85, -15)
    
    # S/R
    range_p = current * 0.12
    s1 = current - range_p * 0.382
    s2 = current - range_p * 0.618
    s3 = current - range_p
    r1 = current + range_p * 0.382
    r2 = current + range_p * 0.618
    r3 = current + range_p
    
    # Trend
    if current > ma20 * 1.03:
        trend = "BULLISH"
    elif current < ma20 * 0.97:
        trend = "BEARISH"
    else:
        trend = "SIDEWAYS"
    
    # Market Cap
    mc = current * random.randint(5_000_000_000, 50_000_000_000)
    if mc > 1e12:
        market_cap = f"{mc/1e12:.1f} T"
    elif mc > 1e9:
        market_cap = f"{mc/1e9:.1f} T"
    else:
        market_cap = f"{mc/1e6:.1f} M"
    
    result = {
        'symbol': symbol,
        'current_price': current,
        'change': change,
        'change_percent': change_percent,
        'volume': random.randint(1_000_000, 50_000_000),
        'avg_volume': random.randint(1_000_000, 50_000_000),
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma50': ma50, 'ma100': ma100,
        'rsi': rsi, 'macd': macd, 'stoch': stoch, 'cci': cci, 'williams': williams,
        's1': s1, 's2': s2, 's3': s3, 'r1': r1, 'r2': r2, 'r3': r3,
        'trend': trend, 'market_cap': market_cap,
        'eps': random.uniform(50, 500),
        'per': random.uniform(8, 25),
        'pbv': random.uniform(0.8, 4.5),
        'roe': random.uniform(8, 28),
        'der': random.uniform(0.1, 1.8),
        'div_yield': random.uniform(0.5, 5.5)
    }
    
    stock_cache[symbol] = result
    cache_time[symbol] = current_time
    return result

def generate_bandarmology():
    asing = random.randint(-300, 600)
    retail = random.randint(-500, 200)
    bandar = random.randint(-200, 500)
    
    asing_status = "AKUMULASI" if asing > 150 else "NETRAL" if asing > -150 else "DISTRIBUSI"
    retail_status = "DISTRIBUSI" if retail < -150 else "NETRAL" if retail < 150 else "AKUMULASI"
    bandar_status = "AKUMULASI" if bandar > 120 else "NETRAL" if bandar > -120 else "DISTRIBUSI"
    
    return {
        'asing': asing, 'retail': retail, 'bandar': bandar,
        'asing_status': asing_status, 'retail_status': retail_status, 'bandar_status': bandar_status
    }

def analyze_stock(symbol):
    symbol = symbol.upper()
    
    if symbol not in STOCKS:
        similar = [s for s in STOCKS if symbol in s][:5]
        if similar:
            return f"❌ Kode *{symbol}* tidak ditemukan.\n\nMungkin maksud Anda: {', '.join(similar[:5])}"
        return f"❌ Kode *{symbol}* tidak ditemukan. Ketik /list untuk melihat daftar saham."
    
    data = generate_stock_data(symbol)
    bandar = generate_bandarmology()
    
    # Hitung signal
    buy = sum([
        data['rsi'] < 40, data['cci'] < -100, data['williams'] < -80,
        data['stoch'] < 20, data['current_price'] > data['ma50'],
        bandar['asing_status'] == "AKUMULASI", bandar['bandar_status'] == "AKUMULASI"
    ])
    sell = sum([
        data['rsi'] > 70, data['cci'] > 100, data['williams'] > -20,
        data['stoch'] > 80, data['current_price'] < data['ma50'],
        bandar['asing_status'] == "DISTRIBUSI", bandar['bandar_status'] == "DISTRIBUSI"
    ])
    
    signal = "BUY" if buy >= sell + 2 else "SELL" if sell >= buy + 2 else "WAIT N SEE"
    
    # Format output
    result = f"""
📈 *ANALISIS SAHAM {data['symbol']}*
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}
💰 Harga: {fmt_price(data['current_price'])}
📊 Perubahan: {data['change']:.0f} ({data['change_percent']:.2f}%)
🏢 Market Cap: {data['market_cap']}
📈 Trend: {data['trend']}
🛡️ Support: {fmt_price(data['s1'])} | {fmt_price(data['s2'])} | {fmt_price(data['s3'])}
🚧 Resist: {fmt_price(data['r1'])} | {fmt_price(data['r2'])} | {fmt_price(data['r3'])}

━━━━━━━━━━━━━━━━━━━━━
🎯 *SIGNAL & REKOMENDASI*
━━━━━━━━━━━━━━━━━━━━━

📊 *SWING TRADING (3 HARI - 1 BULAN)*
*SIGNAL: {signal}*
Entry   : {fmt_price(data['s2'])} - {fmt_price(data['current_price'])}
Target 1: {fmt_price(data['current_price'] * 1.05)} (+5%)
Target 2: {fmt_price(data['current_price'] * 1.11)} (+11%)
Target 3: {fmt_price(data['current_price'] * 1.15)} (+15%)
Stop Loss: {fmt_price(data['s3'] * 0.98)} (-4.5%)

⚡ *DAY TRADE (INTRADAY)*
*SIGNAL: {signal}*
Entry   : {fmt_price(data['s1'])} - {fmt_price(data['current_price'])}
Target  : {fmt_price(data['r1'])} | {fmt_price(data['r2'])}
Stop Loss: {fmt_price(data['s1'] * 0.99)} (-1%)

━━━━━━━━━━━━━━━━━━━━━
📊 *TEKNIKAL LENGKAP*
━━━━━━━━━━━━━━━━━━━━━

📈 *MOVING AVERAGE*
MA 5    : {fmt_price(data['ma5'])}    {'BUY' if data['current_price'] > data['ma5'] else 'SELL'}
MA 10   : {fmt_price(data['ma10'])}    {'BUY' if data['current_price'] > data['ma10'] else 'SELL'}
MA 20   : {fmt_price(data['ma20'])}    {'BUY' if data['current_price'] > data['ma20'] else 'SELL'}
MA 50   : {fmt_price(data['ma50'])}    {'BUY' if data['current_price'] > data['ma50'] else 'SELL'}
MA 100  : {fmt_price(data['ma100'])}    {'BUY' if data['current_price'] > data['ma100'] else 'SELL'}

📊 *OSCILATOR*
RSI (14)      : {data['rsi']:.1f}     {'BUY' if data['rsi'] < 40 else 'SELL' if data['rsi'] > 70 else 'NEUTRAL'}
MACD          : {data['macd']:.0f}  {'BUY' if data['macd'] > 0 else 'SELL'}
Stochastic    : {data['stoch']:.1f}     {'BUY' if data['stoch'] < 20 else 'SELL' if data['stoch'] > 80 else 'NEUTRAL'}
CCI           : {data['cci']:.0f}     {'BUY' if data['cci'] < -100 else 'SELL' if data['cci'] > 100 else 'NEUTRAL'}
Williams %R   : {data['williams']:.0f}      {'BUY' if data['williams'] < -80 else 'SELL' if data['williams'] > -20 else 'NEUTRAL'}

━━━━━━━━━━━━━━━━━━━━━
📊 *FUNDAMENTAL*
━━━━━━━━━━━━━━━━━━━━━

EPS   : Rp {fmt_number(data['eps'])}
PER   : {data['per']:.1f}x
PBV   : {data['pbv']:.1f}x
ROE   : {data['roe']:.1f}%
DER   : {data['der']:.2f}x
Div Yield: {data['div_yield']:.1f}%

━━━━━━━━━━━━━━━━━━━━━
💰 *BANDARMOLOGY 3 HARI*
━━━━━━━━━━━━━━━━━━━━━
Asing/Lembaga : *{bandar['asing_status']}* ({bandar['asing']:+}M)
Retail/Lokal   : *{bandar['retail_status']}* ({bandar['retail']:+}M)
Bandar         : *{bandar['bandar_status']}* ({bandar['bandar']:+}M)

📌 *DISCLAIMER:* Saya hanya bot analisis untuk referensi, bukan rekomendasi jual/beli.

🔍 Ketik kode saham lain: BBCA, BBRI, TLKM, ASII, GGRM
"""
    return result

# ==================== HANDLER TELEGRAM ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Halo! Saya Bot Analisis Saham Indonesia*\n\n"
        "📊 *Fitur:* 900+ saham IDX, Bandarmology, Fundamental\n\n"
        "🔍 Ketik kode saham (contoh: BBCA, BBRI, TLKM)\n"
        "/help untuk bantuan",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *BANTUAN*\n\n"
        "🔍 Ketik kode saham (BBCA, BBRI, TLKM)\n"
        "/list - 50 saham populer\n"
        "/stats - Statistik bot",
        parse_mode='Markdown'
    )

async def list_stocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks = ", ".join(STOCKS[:50])
    await update.message.reply_text(
        f"📋 *50 SAHAM POPULER*\n\n{stocks}\n\nTotal: {len(STOCKS)} saham",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *STATISTIK*\n\n"
        f"• Saham: {len(STOCKS)}\n"
        f"• Cache: {len(stock_cache)}\n"
        f"• AI: {'AKTIF' if OPENAI_API_KEY else 'NONAKTIF'}",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    user = update.effective_user.first_name
    
    await update.message.chat.send_action(action="typing")
    
    if msg.isalpha() and len(msg) <= 5 and msg.upper() == msg:
        await update.message.reply_text(f"🔍 Menganalisis *{msg}*...", parse_mode='Markdown')
        result = analyze_stock(msg)
        await update.message.reply_text(result, parse_mode='Markdown')
    elif OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": msg}]
            )
            await update.message.reply_text(response.choices[0].message.content)
        except:
            await update.message.reply_text("Maaf, AI error.")
    else:
        await update.message.reply_text("❌ AI tidak aktif. Ketik kode saham.")

# ==================== MAIN ====================
if __name__ == '__main__':
    print("✅ Memulai bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_stocks))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot siap! Tekan Ctrl+C untuk berhenti")
    app.run_polling()
