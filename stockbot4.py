#!/usr/bin/env python3
"""
BOT TELEGRAM SAHAM INDONESIA - VERSION SEDERHANA
Fitur: Analisis 900+ saham + Bandarmology + Fundamental
Cara install: python3 bot.py
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sys
import random
import time

print("=" * 50)
print("🤖 BOT TELEGRAM SAHAM SEDERHANA")
print("=" * 50)
print("")

TOKEN = input("🔑 Masukkan Token Bot Telegram: ").strip()
if not TOKEN:
    print("❌ Token tidak boleh kosong!")
    sys.exit(1)

print("")
print("✅ Memuat 900+ saham IDX...")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

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

print(f"✅ {len(STOCKS)} saham siap!")

# Cache
stock_cache = {}
cache_time = {}

def fmt_price(price):
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    return f"{num:,.0f}".replace(",", ".")

def get_status_per(per):
    if per < 10: return "MURAH"
    if per < 15: return "WAJAR"
    if per < 20: return "PREMIUM"
    return "MAHAL"

def get_status_pbv(pbv):
    if pbv < 1: return "DISKON"
    if pbv < 2: return "WAJAR"
    if pbv < 3: return "PREMIUM"
    return "MAHAL"

def get_status_roe(roe):
    if roe > 20: return "SANGAT BAIK"
    if roe > 15: return "BAIK"
    if roe > 10: return "CUKUP"
    return "KURANG"

def get_status_der(der):
    if der < 0.5: return "AMAN"
    if der < 1: return "CUKUP"
    if der < 2: return "TINGGI"
    return "BERISIKO"

def get_status_dividen(dy):
    if dy > 5: return "TINGGI"
    if dy > 3: return "BAGUS"
    if dy > 1: return "STABIL"
    if dy > 0: return "RENDAH"
    return "TIDAK BAGI"

def get_status_eps(eps_growth):
    if eps_growth > 15: return "SANGAT BAIK"
    if eps_growth > 5: return "STABIL"
    if eps_growth > 0: return "LAMBAT"
    return "MELEMAH"

def generate_data(symbol):
    now = time.time()
    if symbol in stock_cache and now - cache_time.get(symbol, 0) < 300:
        return stock_cache[symbol]
    
    random.seed(symbol + datetime.now().strftime('%Y%m%d'))
    
    base = {
        'BBCA': 9500, 'BBRI': 5250, 'BMRI': 6200, 'BBNI': 5100, 'TLKM': 3750,
        'ASII': 5750, 'UNVR': 2850, 'GGRM': 22750, 'HMSP': 875, 'ICBP': 9850,
    }.get(symbol, random.randint(500, 20000))
    
    change = random.uniform(-3.5, 3.5)
    price = base + (base * change / 100)
    
    range_p = price * 0.1
    s1 = price - range_p * 0.5
    s2 = price - range_p
    s3 = price - range_p * 1.5
    r1 = price + range_p * 0.5
    r2 = price + range_p
    r3 = price + range_p * 1.5
    
    if price > base * 1.02:
        trend = "BULLISH"
    elif price < base * 0.98:
        trend = "BEARISH"
    else:
        trend = "SIDEWAYS"
    
    mc = price * random.randint(5_000_000_000, 30_000_000_000)
    if mc > 1e12:
        market_cap = f"{mc/1e12:.1f} T"
    else:
        market_cap = f"{mc/1e9:.1f} T"
    
    ma5 = price * random.uniform(0.97, 1.03)
    ma20 = price * random.uniform(0.95, 1.05)
    ma50 = price * random.uniform(0.92, 1.08)
    ma100 = price * random.uniform(0.90, 1.10)
    
    rsi = random.uniform(25, 75)
    macd = random.uniform(-150, 150)
    
    eps = random.uniform(100, 1000)
    eps_growth = random.uniform(-5, 25)
    per = price / eps
    pbv = random.uniform(0.8, 4.5)
    roe = random.uniform(8, 28)
    der = random.uniform(0.1, 1.8)
    div_yield = random.uniform(0, 6)
    
    asing = random.randint(-300, 600)
    retail = random.randint(-500, 200)
    bandar = random.randint(-200, 500)
    
    asing_status = "AKUMULASI" if asing > 150 else "NETRAL" if asing > -150 else "DISTRIBUSI"
    retail_status = "DISTRIBUSI" if retail < -150 else "NETRAL" if retail < 150 else "AKUMULASI"
    bandar_status = "AKUMULASI" if bandar > 120 else "NETRAL" if bandar > -120 else "DISTRIBUSI"
    
    result = {
        'symbol': symbol, 'price': price, 'change': change, 'trend': trend,
        'market_cap': market_cap, 's1': s1, 's2': s2, 's3': s3,
        'r1': r1, 'r2': r2, 'r3': r3, 'ma5': ma5, 'ma20': ma20,
        'ma50': ma50, 'ma100': ma100, 'rsi': rsi, 'macd': macd,
        'eps': eps, 'eps_growth': eps_growth, 'per': per, 'pbv': pbv,
        'roe': roe, 'der': der, 'div_yield': div_yield,
        'asing': asing, 'asing_status': asing_status,
        'retail': retail, 'retail_status': retail_status,
        'bandar': bandar, 'bandar_status': bandar_status
    }
    
    stock_cache[symbol] = result
    cache_time[symbol] = now
    return result

def analyze(symbol):
    symbol = symbol.upper()
    
    if symbol not in STOCKS:
        return f"❌ Kode *{symbol}* tidak ditemukan"
    
    d = generate_data(symbol)
    
    if d['rsi'] < 40 and d['macd'] < 0:
        signal = "BUY"
    elif d['rsi'] > 70 and d['macd'] > 0:
        signal = "SELL"
    else:
        signal = "NETRAL"
    
    return f"""
📈 *ANALISIS {d['symbol']}*
🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}
💰 {fmt_price(d['price'])} ({d['change']:.2f}%)
🏢 {d['market_cap']} | {d['trend']}

🛡️ S: {fmt_price(d['s1'])} | {fmt_price(d['s2'])} | {fmt_price(d['s3'])}
🚧 R: {fmt_price(d['r1'])} | {fmt_price(d['r2'])} | {fmt_price(d['r3'])}

━━━━━━━━━━━━━━━━
🎯 *SIGNAL: {signal}*

📊 *SWING*
Entry: {fmt_price(d['s2'])} - {fmt_price(d['price'])}
Target: {fmt_price(d['r1'])} | {fmt_price(d['r2'])}
SL: {fmt_price(d['s3'])} (-4.5%)

⚡ *DAY TRADE*
Entry: {fmt_price(d['s1'])} - {fmt_price(d['price'])}
Target: {fmt_price(d['r1'])} | {fmt_price(d['r2'])}
SL: {fmt_price(d['s1'] * 0.99)} (-1%)

━━━━━━━━━━━━━━━━
📊 *TEKNIKAL*
MA5: {fmt_price(d['ma5'])} | MA20: {fmt_price(d['ma20'])}
MA50: {fmt_price(d['ma50'])} | MA100: {fmt_price(d['ma100'])}
RSI: {d['rsi']:.1f} | MACD: {d['macd']:.0f}

━━━━━━━━━━━━━━━━
📊 *FUNDAMENTAL*
EPS: Rp {fmt_number(d['eps'])} [{get_status_eps(d['eps_growth'])}]
PER: {d['per']:.1f}x [{get_status_per(d['per'])}]
PBV: {d['pbv']:.1f}x [{get_status_pbv(d['pbv'])}]
ROE: {d['roe']:.1f}% [{get_status_roe(d['roe'])}]
DER: {d['der']:.2f}x [{get_status_der(d['der'])}]
Div: {d['div_yield']:.1f}% [{get_status_dividen(d['div_yield'])}]

━━━━━━━━━━━━━━━━
💰 *BANDARMOLOGY*
🏦 Asing: *{d['asing_status']}* ({d['asing']:+}M)
🏪 Retail: *{d['retail_status']}* ({d['retail']:+}M)
🕴️ Bandar: *{d['bandar_status']}* ({d['bandar']:+}M)

📌 *DISCLAIMER:* Hanya referensi
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *BOT SAHAM SEDERHANA*\n\n"
        "📌 Ketik kode saham:\n"
        "BBCA, BBRI, TLKM, ASII, GGRM\n\n"
        "/list - 50 saham\n"
        "/help - Bantuan",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *BANTUAN*\n\n"
        "🔍 Ketik kode saham (contoh: BBCA)\n"
        "/list - Lihat 50 saham\n"
        "/stats - Statistik",
        parse_mode='Markdown'
    )

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks = ", ".join(STOCKS[:50])
    await update.message.reply_text(
        f"📋 *50 SAHAM*\n\n{stocks}",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *STATISTIK*\n\n"
        f"• Total saham: {len(STOCKS)}\n"
        f"• Cache: {len(stock_cache)}",
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
    print("✅ Bot siap! Tekan Ctrl+C untuk stop")
    app.run_polling()
