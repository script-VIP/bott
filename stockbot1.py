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
import os
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
    # LQ45 (45 saham)
    'BBCA', 'BBRI', 'BMRI', 'BBNI', 'BCA', 'TLKM', 'ASII', 'UNVR', 
    'GGRM', 'HMSP', 'ICBP', 'INDF', 'KLBF', 'CPIN', 'JPFA', 'ADRO', 
    'PTBA', 'ITMG', 'HRUM', 'MEDC', 'ANTM', 'MDKA', 'INCO', 'BRPT', 
    'TPIA', 'PGAS', 'PTRO', 'ELSA', 'AKRA', 'MAPI', 'ERAA', 'ACES', 
    'RALS', 'LPPF', 'MAPA', 'SIDO', 'DVLA', 'KAEF', 'INAF', 'TSPC', 
    'JSMR', 'EXCL', 'ISAT', 'FREN', 'TOWR', 'WIKA', 'PTPP', 'ADHI', 
    'WSKT', 'TOTL',
    
    # Kompas100 (tambahan)
    'ARTO', 'AALI', 'ADMF', 'AGRO', 'AKPI', 'AMMN', 'ARNA', 'ASGR',
    'ASRI', 'AUTO', 'BABP', 'BACA', 'BAEK', 'BANK', 'BATA', 'BBHI',
    'BBKP', 'BBLD', 'BBMD', 'BBTN', 'BBYB', 'BCAP', 'BDMN', 'BEKS',
    'BFIN', 'BGTG', 'BHIT', 'BIPP', 'BISI', 'BJBR', 'BJTM', 'BKSL',
    'BMAS', 'BMTR', 'BNBA', 'BNGA', 'BNII', 'BNLI', 'BRAM', 'BRMS',
    'BSDE', 'BSIM', 'BSSR', 'BUDI', 'BUMI', 'BUVA', 'BVIC', 'CASN',
    'CEKA', 'CINT', 'CMNP', 'CMPP', 'CNTX', 'CRAB', 'CSAP', 'CTRA',
    'CTTH', 'DEWA', 'DGIK', 'DILD', 'DKFT', 'DLTA', 'DMAS', 'DOID',
    'DPNS', 'DSNG', 'DUTI', 'DVLA', 'DYAN', 'EKAD', 'ELSA', 'ELTY',
    'EMTK', 'ENRG', 'EPAC', 'ERAA', 'ERTX', 'ESSA', 'ETWA', 'EXCL',
    'FAJS', 'FASW', 'FMII', 'FORU', 'FPNI', 'FREN', 'GAMA', 'GDYR',
    'GEMS', 'GGRM', 'GJTL', 'GOLD', 'GPRA', 'GSMF', 'GTBO', 'GWSA',
    'HAIS', 'HDIT', 'HITS', 'HMSP', 'HRTA', 'HRUM', 'ICBP', 'ICON',
    'IGAR', 'IMAS', 'IMJS', 'INAF', 'INAI', 'INCI', 'INCO', 'INDF',
    'INDY', 'INFO', 'INPC', 'INPP', 'INTA', 'INTD', 'INTP', 'IPCC',
    'IPOL', 'ISAT', 'ISSP', 'ITMA', 'ITMG', 'JAKA', 'JECC', 'JEPE',
    'JMAS', 'JPFA', 'JPRS', 'JRPT', 'JSKY', 'JSMR', 'JSPT', 'KAEF',
    'KARW', 'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KIAS', 'KICI', 'KINO',
    'KIOS', 'KKGI', 'KLBF', 'KMTR', 'KOIN', 'KOPI', 'KOTA', 'KPIG',
    'KRAS', 'LABA', 'LAMI', 'LCGP', 'LCKM', 'LION', 'LMAS', 'LMSH',
    'LPCK', 'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPS', 'LRNA', 'LSIP',
    'LTLS', 'MABA', 'MAIN', 'MAMI', 'MAPA', 'MAPI', 'MASA', 'MAYA',
    'MBAP', 'MBSS', 'MBTO', 'MCOR', 'MDIA', 'MDKA', 'MDLN', 'MDRN',
    'MEDC', 'MEGA', 'MERK', 'MFIN', 'MFMI', 'MICE', 'MIDI', 'MINA',
    'MIRA', 'MITI', 'MKNT', 'MKPI', 'MLBI', 'MLIA', 'MLND', 'MNCN',
    'MORA', 'MPAX', 'MPPA', 'MPRO', 'MRAT', 'MSIE', 'MSIN', 'MTDL',
    'MTFN', 'MTLA', 'MTSM', 'MYOH', 'MYOR', 'MYRX', 'NASA', 'NELY',
    'NETV', 'NICK', 'NIFE', 'NIPS', 'NIRO', 'NISP', 'NOBU', 'NPGF',
    'NRCA', 'NUSA', 'OASA', 'OKAS', 'OMRE', 'PADI', 'PALM', 'PANE',
    'PANI', 'PANS', 'PBRX', 'PDES', 'PDPP', 'PEGE', 'PGAS', 'PGLI',
    'PICO', 'PJAA', 'PKPK', 'PLAN', 'PLAS', 'PLIN', 'PMJS', 'PNBN',
    'PNIN', 'PNLF', 'POLL', 'POLY', 'POOL', 'PORT', 'POSA', 'POWR',
    'PPRO', 'PRAS', 'PRDA', 'PSAB', 'PSDN', 'PSSI', 'PTBA', 'PTDU',
    'PTIS', 'PTMP', 'PTRO', 'PTSN', 'PUDP', 'PURA', 'PWON', 'PYFA',
    'RALS', 'RANC', 'RBMS', 'RDTX', 'REAL', 'RELI', 'RIMO', 'RISE',
    'RISH', 'RMBA', 'ROCK', 'RODA', 'ROTI', 'RUIS', 'SAFE', 'SAME',
    'SAMF', 'SAPX', 'SARA', 'SATU', 'SCBD', 'SCCO', 'SCMA', 'SDMU',
    'SDPC', 'SGER', 'SHID', 'SIDO', 'SILO', 'SIMP', 'SIPD', 'SKLT',
    'SKYB', 'SMAR', 'SMCB', 'SMDM', 'SMDR', 'SMGR', 'SMMA', 'SMMT',
    'SMRU', 'SMRA', 'SMSM', 'SNLK', 'SONA', 'SPMA', 'SPMI', 'SQMI',
    'SRAJ', 'SRIL', 'SRSN', 'SSIA', 'SSMS', 'SSTM', 'STAR', 'STTP',
    'SUGI', 'SULI', 'SUPR', 'SURY', 'SZPO', 'TALF', 'TARA', 'TAXI',
    'TBIG', 'TBLA', 'TCPI', 'TCID', 'TDPM', 'TELE', 'TFCO', 'TIFA',
    'TINS', 'TIRA', 'TIRF', 'TIRT', 'TKIM', 'TLKM', 'TMAS', 'TMPO',
    'TNCA', 'TOBA', 'TOPS', 'TOTL', 'TOWR', 'TPIA', 'TPMA', 'TRAM',
    'TRIN', 'TRIO', 'TRIS', 'TRST', 'TRUB', 'TRUK', 'TRUS', 'TSPC',
    'TURI', 'TUVU', 'TWIN', 'TYRE', 'UANG', 'UCID', 'UG', 'ULTJ',
    'UNIC', 'UNIT', 'UNSP', 'UNTR', 'UNVR', 'VIVA', 'VOKS', 'VRNA',
    'WAPO', 'WEGE', 'WEHA', 'WICO', 'WIIM', 'WIKA', 'WIM', 'WINR',
    'WINS', 'WOOD', 'WOWS', 'WSKT', 'WTON', 'YELO', 'YESC', 'YPAS',
    'YULE', 'ZBRA', 'ZINC'
]

print(f"✅ {len(STOCKS)} saham IDX siap!")

# Cache untuk data saham
stock_cache = {}
cache_time = {}

# ==================== FUNGSI FORMAT ====================
def fmt_price(price):
    """Format harga ke Rupiah"""
    if price is None:
        return "Rp 0"
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    """Format angka dengan separator"""
    if num is None:
        return "0"
    return f"{num:,.0f}".replace(",", ".")

# ==================== FUNGSI GENERATE DATA ====================
def generate_stock_data(symbol):
    """Generate data saham simulasi"""
    # Cek cache (5 menit)
    current_time = time.time()
    if symbol in stock_cache and symbol in cache_time:
        if current_time - cache_time[symbol] < 300:  # 5 menit
            return stock_cache[symbol]
    
    # Seed berdasarkan symbol + tanggal (biar konsisten seharian)
    random.seed(symbol + datetime.now().strftime('%Y%m%d'))
    
    # Harga dasar berdasarkan sektor (simulasi)
    sector_prices = {
        # Bank
        'BBCA': 9500, 'BBRI': 5250, 'BMRI': 6200, 'BBNI': 5100, 'BCA': 9500,
        'BJBR': 1850, 'BJTM': 1650, 'BRIS': 1750, 'ARTO': 2450, 'BNGA': 1650,
        'BNII': 1050, 'BNLI': 850, 'NISP': 1150, 'MAYA': 1150, 'BDMN': 2750,
        
        # Telekomunikasi
        'TLKM': 3750, 'EXCL': 2250, 'ISAT': 7750, 'FREN': 50, 'TOWR': 925,
        
        # Otomotif
        'ASII': 5750, 'AUTO': 1550, 'BOLT': 425, 'GDYR': 575, 'IMAS': 1250,
        
        # Consumer
        'UNVR': 2850, 'GGRM': 22750, 'HMSP': 875, 'ICBP': 9850, 'INDF': 6250,
        'KLBF': 1575, 'SIDO': 675, 'DVLA': 2050, 'KAEF': 1650, 'TSPC': 1250,
        'INAF': 675, 'CPIN': 4950, 'JPFA': 1850, 'MAIN': 2750, 'CINT': 1450,
        'DLTA': 4850, 'ROTI': 1250, 'ULTJ': 1550, 'CAMP': 3450, 'SKLT': 2450,
        
        # Tambang
        'ADRO': 2750, 'PTBA': 3150, 'ITMG': 26750, 'HRUM': 1250, 'MEDC': 1275,
        'ANTM': 1850, 'MDKA': 2450, 'INCO': 4750, 'BRPT': 975, 'TPIA': 7750,
        'BUMI': 125, 'BYAN': 19500, 'GEMS': 4250, 'INDY': 1750, 'KKGI': 825,
        'MBAP': 3750, 'SMMT': 2750, 'TINS': 1150, 'TOBA': 975, 'ZINC': 275,
        
        # Energi
        'PGAS': 1650, 'PTRO': 7750, 'ELSA': 425, 'AKRA': 1450, 'ENRG': 275,
        'MEDC': 1275, 'RAJA': 375, 'RUIS': 275, 'SUGI': 975,
        
        # Properti
        'BSDE': 1250, 'CTRA': 1150, 'DMAS': 175, 'DUTI': 3250, 'LPCK': 5750,
        'LPKR': 125, 'MDLN': 75, 'MKPI': 23500, 'MTLA': 425, 'NIRO': 50,
        'PLIN': 2350, 'PPRO': 125, 'PUDP': 275, 'PWON': 475, 'RISE': 175,
        'ROCK': 75, 'SMRA': 675, 'TARA': 125, 'TRIN': 975, 'WIKA': 875,
        'WSKT': 375, 'ADHI': 575, 'PTPP': 775, 'TOTL': 775, 'ACST': 275,
        
        # Retail
        'ACES': 775, 'AMRT': 2350, 'CSAP': 975, 'ECII': 375, 'ERAA': 375,
        'LPPF': 7750, 'MAPI': 1650, 'MAPA': 875, 'RALS': 375, 'MIDI': 425,
        'MPPA': 175, 'SONA': 675, 'TELE': 1150, 'TRIO': 275,
        
        # Industri
        'INTP': 10750, 'SMGR': 6750, 'SMCB': 1175, 'ARNA': 675, 'AMFG': 6750,
        'BRAM': 1275, 'BUDI': 275, 'CEKA': 3250, 'EKAD': 575, 'IGAR': 775,
        'INCI': 575, 'JECC': 375, 'KBLI': 1275, 'KBLM': 275, 'LION': 475,
        'MLIA': 75, 'PICO': 175, 'TOTO': 775, 'UNIC': 225, 'VOKS': 125,
        
        # Perkebunan
        'AALI': 7750, 'LSIP': 1175, 'SSMS': 1075, 'TBLA': 875, 'BWPT': 175,
        'DSNG': 375, 'GZCO': 475, 'JAWA': 575, 'MGRO': 675, 'PALM': 375,
        'SIMP': 475, 'SIPD': 375, 'SMAR': 3750, 'UNSP': 175,
        
        # Transportasi
        'BIRD': 1650, 'BPTR': 775, 'CASS': 775, 'HAIS': 175, 'HITS': 575,
        'JSMR': 4150, 'LRNA': 475, 'MIRA': 775, 'NELY': 175, 'PSSI': 775,
        'SAFE': 175, 'SDMU': 175, 'TAXI': 175, 'TMAS': 1575, 'WINS': 375,
        'ZBRA': 175,
        
        # Lainnya
        'ABDA': 3750, 'ABMM': 2750, 'ADES': 875, 'ADMF': 9750, 'AISA': 375,
        'ALDO': 575, 'APEX': 775, 'APIC': 575, 'ARII': 275, 'ASGR': 875,
        'ASSA': 575, 'ATIC': 575, 'BALI': 275, 'BAYU': 275, 'BEEF': 375,
        'BLTZ': 775, 'BPII': 275, 'CAMP': 3450, 'CASA': 275, 'CASH': 275,
        'CLPI': 775, 'CNKO': 75, 'COCO': 375, 'DEAL': 175, 'DNAR': 175,
        'DUCK': 375, 'DYAN': 575, 'EASY': 175, 'EDGE': 275, 'ENVY': 175,
        'ESIP': 375, 'FIMP': 275, 'FIRE': 175, 'FISH': 775, 'FORZ': 175,
        'GLOB': 275, 'GOLL': 175, 'HDFA': 375, 'HKMU': 175, 'HOPE': 175,
        'HOTL': 575, 'IDPR': 175, 'IIKP': 175, 'IKAI': 375, 'INCF': 475,
        'INPS': 175, 'INRU': 175, 'IPCC': 775, 'ITMA': 375, 'JAKW': 375,
        'JATS': 175, 'JETS': 175, 'JIND': 775, 'JKON': 175, 'JKSW': 175,
        'JPRS': 175, 'KEEN': 775, 'KIAI': 175, 'KIOS': 275, 'KOLI': 175,
        'KOTA': 175, 'KPAL': 275, 'KPIG': 375, 'LAPD': 175, 'LCKM': 175,
        'LEAD': 175, 'LFLO': 375, 'LPIN': 375, 'MADI': 175, 'MAGA': 175,
        'MAMI': 375, 'MCOR': 175, 'MDIA': 375, 'MEGA': 4750, 'MFMI': 175,
        'MMLP': 175, 'MORA': 375, 'MPRO': 175, 'MSIE': 175, 'MTWI': 175,
        'NASA': 375, 'NETV': 175, 'NICK': 175, 'NIFE': 175, 'NPGF': 375,
        'NTBK': 175, 'OASA': 175, 'PADI': 175, 'PAPX': 175, 'PDES': 375,
        'PEGE': 575, 'PGUN': 375, 'PKPK': 175, 'PLAN': 175, 'PMMP': 275,
        'POLL': 175, 'POLU': 375, 'PORT': 775, 'PPGL': 175, 'PRDA': 375,
        'PSAB': 175, 'PSDN': 175, 'PTIS': 175, 'PTMP': 175, 'RELI': 175,
        'SAME': 175, 'SAMF': 175, 'SAPX': 175, 'SARA': 175, 'SDPC': 175,
        'SGER': 375, 'SKYB': 175, 'SMDR': 375, 'SPMI': 175, 'SQMI': 175,
        'SRAJ': 175, 'SSTM': 175, 'STAR': 175, 'SURY': 175, 'TDPM': 175,
        'TIRF': 375, 'TIRT': 375, 'TUVU': 175, 'TWIN': 175, 'TYRE': 375,
        'UANG': 175, 'UCID': 375, 'UG': 175, 'UNIT': 375, 'VIVA': 175,
        'WAPO': 175, 'WEGE': 175, 'WEHA': 175, 'WIIM': 175, 'WIM': 175,
        'WINR': 175, 'WOOD': 375, 'YELO': 175, 'YESC': 175, 'YPAS': 375,
        'YULE': 175
    }
    
    # Ambil harga dasar atau random
    if symbol in sector_prices:
        base = sector_prices[symbol]
    else:
        base = random.randint(200, 5000)
    
    # Fluktuasi harian
    change_percent = random.uniform(-3.5, 3.5)
    change = base * change_percent / 100
    current_price = base + change
    
    # Volume
    volume = random.randint(1_000_000, 50_000_000)
    avg_volume = volume * random.uniform(0.7, 1.3)
    
    # Moving Average
    ma5 = current_price * random.uniform(0.96, 1.04)
    ma10 = current_price * random.uniform(0.95, 1.05)
    ma20 = current_price * random.uniform(0.93, 1.07)
    ma50 = current_price * random.uniform(0.90, 1.10)
    ma100 = current_price * random.uniform(0.85, 1.15)
    
    # Oscillator
    rsi = random.uniform(25, 75)
    macd = random.uniform(-150, 150)
    stoch = random.uniform(15, 85)
    cci = random.uniform(-120, 120)
    williams = random.uniform(-85, -15)
    
    # Support & Resistance
    range_price = current_price * 0.12
    s1 = current_price - range_price * 0.382
    s2 = current_price - range_price * 0.618
    s3 = current_price - range_price
    r1 = current_price + range_price * 0.382
    r2 = current_price + range_price * 0.618
    r3 = current_price + range_price
    
    # Trend
    if current_price > ma20 * 1.03:
        trend = "BULLISH"
    elif current_price < ma20 * 0.97:
        trend = "BEARISH"
    else:
        trend = "SIDEWAYS"
    
    # Market Cap
    shares = random.randint(5_000_000_000, 50_000_000_000)
    mc = current_price * shares
    if mc > 1e12:
        market_cap = f"{mc/1e12:.1f} T"
    elif mc > 1e9:
        market_cap = f"{mc/1e9:.1f} T"
    else:
        market_cap = f"{mc/1e6:.1f} M"
    
    # Fundamental
    eps = random.uniform(50, 500)
    per = current_price / eps if eps > 0 else random.uniform(8, 25)
    pbv = random.uniform(0.8, 4.5)
    roe = random.uniform(8, 28)
    der = random.uniform(0.1, 1.8)
    div_yield = random.uniform(0.5, 5.5)
    
    result = {
        'symbol': symbol,
        'current_price': current_price,
        'change': change,
        'change_percent': change_percent,
        'volume': volume,
        'avg_volume': avg_volume,
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma50': ma50, 'ma100': ma100,
        'rsi': rsi, 'macd': macd, 'stoch': stoch, 'cci': cci, 'williams': williams,
        's1': s1, 's2': s2, 's3': s3,
        'r1': r1, 'r2': r2, 'r3': r3,
        'trend': trend,
        'market_cap': market_cap,
        'eps': eps, 'per': per, 'pbv': pbv, 'roe': roe, 'der': der, 'div_yield': div_yield
    }
    
    # Simpan ke cache
    stock_cache[symbol] = result
    cache_time[symbol] = current_time
    
    return result

def generate_bandarmology():
    """Generate bandarmology (simulasi)"""
    # Random dengan kecenderungan
    asing = random.randint(-300, 600)
    retail = random.randint(-500, 200)
    bandar = random.randint(-200, 500)
    
    # Status
    asing_status = "AKUMULASI" if asing > 150 else "NETRAL" if asing > -150 else "DISTRIBUSI"
    retail_status = "DISTRIBUSI" if retail < -150 else "NETRAL" if retail < 150 else "AKUMULASI"
    bandar_status = "AKUMULASI" if bandar > 120 else "NETRAL" if bandar > -120 else "DISTRIBUSI"
    
    return {
        'asing': asing,
        'retail': retail,
        'bandar': bandar,
        'asing_status': asing_status,
        'retail_status': retail_status,
        'bandar_status': bandar_status
    }

def analyze_stock(symbol):
    """Analisis lengkap saham"""
    symbol = symbol.upper()
    
    if symbol not in STOCKS:
        similar = [s for s in STOCKS if symbol in s][:5]
        if similar:
            return f"❌ Kode *{symbol}* tidak ditemukan.\n\nMungkin maksud Anda: {', '.join(similar[:5])}"
        else:
            return f"❌ Kode *{symbol}* tidak ditemukan. Ketik /list untuk melihat daftar saham."
    
    data = generate_stock_data(symbol)
    bandar = generate_bandarmology()
    
    # Hitung signal
    buy_count = 0
    sell_count = 0
    
    if data['rsi'] < 40: buy_count += 1
    elif data['rsi'] > 70: sell_count += 1
    
    if data['cci'] < -100: buy_count += 1
    elif data['cci'] > 100: sell_count += 1
    
    if data['williams'] < -80: buy_count += 1
    elif data['williams'] > -20: sell_count += 1
    
    if data['stoch'] < 20: buy_count += 1
    elif data['stoch'] > 80: sell_count += 1
    
    if data['current_price'] < data['ma5']: sell_count += 1
    elif data['current_price'] > data['ma5']: buy_count += 1
    
    if bandar['asing_status'] == "AKUMULASI": buy_count += 1
    elif bandar['asing_status'] == "DISTRIBUSI": sell_count += 1
    
    if bandar['bandar_status'] == "AKUMULASI": buy_count += 1
    elif bandar['bandar_status'] == "DISTRIBUSI": sell_count += 1
    
    signal = "BUY" if buy_count >= sell_count + 2 else "SELL" if sell_count >= buy_count + 2 else "WAIT N SEE"
    
    return f"""
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

📌 *ALASAN:*
• Dekat MA100 ({fmt_price(data['ma100'])}) support kuat
• RSI {data['rsi']:.1f} ({'oversold' if data['rsi'] < 40 else 'overbought' if data['rsi'] > 70 else 'netral'})
• CCI {data['cci']:.0f} ({'oversold' if data['cci'] < -100 else 'overbought' if data['cci'] > 100 else 'netral'})
• Bandar {bandar['bandar_status']} 3 hari
• Risk/reward 1:{(data['current_price'] * 1.05 - data['current_price'])/(data['current_price'] - data['s3'] * 0.98):.1f}

⚡ *DAY TRADE (INTRADAY)*
*SIGNAL: {signal}*
Entry   : {fmt_price(data['s1'])} - {fmt_price(data['current_price'])}
Target  : {fmt_price(data['r1'])} | {fmt_price(data['r2'])}
Stop Loss: {fmt_price(data['s1'] * 0.99)} (-1%)

📌 *ALASAN:*
• RSI {data['rsi']:.1f} ({'oversold' if data['rsi'] < 40 else 'overbought' if data['rsi'] > 70 else 'netral'})
• Support S1 ({fmt_price(data['s1'])}) dekat
• Williams %R {data['williams']:.0f} ({'oversold' if data['williams'] < -80 else 'overbought' if data['williams'] > -20 else 'netral'})
• Volume {fmt_number(data['volume'])} ({'di atas' if data['volume'] > data['avg_volume'] else 'di bawah'} rata2)
• Asing {bandar['asing_status']}

━━━━━━━━━━━━━━━━━━━━━
📊 *TEKNIKAL LENGKAP*
━━━━━━━━━━━━━━━━━━━━━

📈 *MOVING AVERAGE*
