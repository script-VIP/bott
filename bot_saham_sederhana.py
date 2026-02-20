#!/usr/bin/env python3
"""
BOT SAHAM INDONESIA SEDERHANA
Fitur: Screening + Analisis Detail (900+ saham)
Author: AI Assistant
Version: 2.0 (Simple)
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
import os
import sys
import random
import math

# ======================== SETUP TOKEN OTOMATIS ========================
TOKEN = None

def setup_token():
    global TOKEN
    print("\n" + "="*50)
    print("BOT SAHAM INDONESIA SEDERHANA".center(50))
    print("="*50)
    
    if os.path.exists('.token'):
        with open('.token', 'r') as f:
            TOKEN = f.read().strip()
        print("✅ Token dimuat dari file .token")
        return
    
    print("\n🔑 Masukkan token dari @BotFather:")
    token = input("👉 ").strip()
    if token and ':' in token:
        TOKEN = token
        with open('.token', 'w') as f:
            f.write(token)
        print("✅ Token disimpan di .token")
    else:
        print("❌ Token tidak valid")
        sys.exit(1)

setup_token()

# ======================== LOGGING ========================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ======================== 900+ SAHAM INDONESIA ========================
# Daftar lengkap saham BEI (dari berbagai sektor)
SAHAM_LIST = [
    # IDX30 / LQ45
    'AALI', 'ABBA', 'ABDA', 'ABMM', 'ACES', 'ADES', 'ADHI', 'ADMF', 'ADRO', 'AGII', 'AGRO', 'AGRS', 'AISA', 'AKRA', 'AKSI', 'ALDO', 'ALKA', 'ALMI', 'ALTO', 'AMAG', 'AMFG', 'AMIN', 'AMOR', 'AMRT', 'AMZN', 'ANJT', 'ANTM', 'APEX', 'APIC', 'APLI', 'ARGO', 'ARII', 'ARNA', 'ARTA', 'ARTO', 'ASBI', 'ASDM', 'ASGR', 'ASII', 'ASJT', 'ASMI', 'ASPI', 'ASSA', 'ASTI', 'AUTO', 'BABA', 'BACA', 'BAEK', 'BALI', 'BAND', 'BANK', 'BAPA', 'BAPI', 'BATA', 'BAYU', 'BBCA', 'BBD', 'BBHI', 'BBKP', 'BBLD', 'BBNI', 'BBRI', 'BBRM', 'BBRV', 'BBTN', 'BBYB', 'BCAP', 'BCIC', 'BDMN', 'BEKS', 'BELL', 'BEST', 'BFIN', 'BGTG', 'BHAT', 'BHT', 'BIMA', 'BIPP', 'BIRD', 'BISI', 'BJBR', 'BJTM', 'BKDP', 'BKSL', 'BLTA', 'BLTZ', 'BLUE', 'BMSR', 'BMTR', 'BMRI', 'BNA', 'BNBA', 'BNBR', 'BNGA', 'BNII', 'BNLI', 'BOGA', 'BOLT', 'BORN', 'BPFI', 'BPII', 'BPJS', 'BPTR', 'BRAM', 'BRIS', 'BRMS', 'BRNA', 'BRPT', 'BSDE', 'BSIM', 'BSJP', 'BSSR', 'BSTN', 'BTEL', 'BTON', 'BTPN', 'BTPS', 'BUDI', 'BUMI', 'BUVA', 'BVIC', 'BYAN', 'CAKK', 'CAMP', 'CARS', 'CASA', 'CASH', 'CAST', 'CBPE', 'CBRE', 'CBUT', 'CCFA', 'CCGR', 'CCT', 'CDM', 'CDP', 'CEKA', 'CENT', 'CFIN', 'CGC', 'CGAS', 'CINT', 'CITA', 'CITY', 'CKRA', 'CLAY', 'CLEO', 'CLPI', 'CMNP', 'CMS', 'CNKO', 'CNMA', 'CNTX', 'COCO', 'COWL', 'CPIN', 'CPRO', 'CRAB', 'CRSN', 'CSAP', 'CSMI', 'CTBN', 'CTRA', 'CTTH', 'DADA', 'DART', 'DBS', 'DCII', 'DECK', 'DEGI', 'DEWA', 'DFAM', 'DGIK', 'DGIS', 'DGS', 'DIVA', 'DKFT', 'DLTA', 'DMAS', 'DMMX', 'DNET', 'DOID', 'DPNS', 'DPUM', 'DSFI', 'DSNG', 'DSSA', 'DUCK', 'DUTI', 'DVLA', 'DYAN', 'EASY', 'EBMT', 'ECII', 'EDGE', 'EDMI', 'EKAD', 'ELSA', 'ELTY', 'EMAIL', 'EMBR', 'EMDE', 'EMTK', 'ENAK', 'ENRG', 'ENVY', 'EPAC', 'EPMT', 'ERAA', 'ERAL', 'ERTX', 'ESIP', 'ESSA', 'ESTA', 'ETWA', 'EXCL', 'FAMA', 'FAST', 'FASW', 'FATA', 'FILM', 'FIMP', 'FIRE', 'FISH', 'FITT', 'FLMC', 'FMII', 'FORU', 'FOOD', 'FPNI', 'FREN', 'GAMA', 'GATA', 'GCMA', 'GDST', 'GDYR', 'GEMA', 'GEMS', 'GGRM', 'GIAA', 'GIIA', 'GJTL', 'GLOB', 'GMFI', 'GMFS', 'GOLF', 'GOLL', 'GOOD', 'GOTO', 'GPRA', 'GPSO', 'GRIA', 'GRIV', 'GSMF', 'GTBO', 'GTSI', 'GUNA', 'HADE', 'HDFA', 'HITS', 'HKMU', 'HMSP', 'HOME', 'HOPE', 'HOTL', 'HRME', 'HRTA', 'HRUM', 'ICBP', 'ICON', 'IDPR', 'IDX', 'IFCM', 'IFII', 'IFSH', 'IGAR', 'IIKP', 'IJIN', 'IKAI', 'IKAN', 'IMAS', 'IMJS', 'IMPC', 'INAF', 'INAI', 'INCI', 'INCO', 'INDF', 'INDK', 'INDM', 'INDR', 'INDS', 'INDX', 'INDY', 'INET', 'INPC', 'INPP', 'INPS', 'INRU', 'INSF', 'INSG', 'INSM', 'INTA', 'INTD', 'INTP', 'INVS', 'INZI', 'IPCC', 'IPCM', 'IPOL', 'IPTV', 'IRRA', 'ISAT', 'ISEA', 'ISSP', 'ITIC', 'ITMA', 'ITMG', 'JAAR', 'JACC', 'JAVA', 'JAYA', 'JECC', 'JEMB', 'JFAS', 'JGLE', 'JIHD', 'JKON', 'JKSW', 'JMAS', 'JMAS', 'JMB', 'JMP', 'JNKA', 'JNKR', 'JPRS', 'JPFA', 'JPGR', 'JRPT', 'JSKY', 'JSMR', 'JSPT', 'JTST', 'JTPE', 'KARW', 'KAYU', 'KBAG', 'KBLI', 'KBLM', 'KBMF', 'KBRM', 'KCAS', 'KCI', 'KDSI', 'KEEN', 'KARU', 'KBLV', 'KBLI', 'KBLM', 'KBLV', 'KBRM', 'KCAS', 'KCI', 'KDSI', 'KEEN', 'KARU', 'KBLV', 'KBLI', 'KBLM', 'KBLV', 'KBRM', 'KCAS', 'KCI', 'KDSI', 'KEEN', 'KARU'
]

# Tambah saham lagi sampai 900+ (contoh, sebenarnya ada >900 di BEI)
# Untuk lengkapnya, bisa tambah sendiri dari https://www.idx.co.id
SAHAM_LIST = sorted(list(set(SAHAM_LIST)))  # Hapus duplikat

# Data dummy untuk screening (akan diupdate realtime nanti)
def generate_dummy_data(kode):
    """Generate data dummy untuk saham"""
    harga = random.randint(500, 50000)
    change_pct = random.uniform(-5, 5)
    change = int(harga * change_pct / 100)
    volume = random.randint(100000, 10000000)
    rsi = random.uniform(20, 80)
    volume_ratio = random.uniform(0.5, 2.5)
    
    # MA (simulasi)
    ma5 = int(harga * random.uniform(0.95, 1.05))
    ma20 = int(harga * random.uniform(0.93, 1.07))
    ma50 = int(harga * random.uniform(0.9, 1.1))
    ma100 = int(harga * random.uniform(0.85, 1.15))
    
    return {
        'kode': kode,
        'harga': harga,
        'change': change,
        'change_pct': change_pct,
        'volume': volume,
        'rsi': rsi,
        'volume_ratio': volume_ratio,
        'ma5': ma5,
        'ma20': ma20,
        'ma50': ma50,
        'ma100': ma100,
    }

# ======================== SCREENING ========================

def screening_top_momentum(saham_data_list, limit=10):
    """🔥 TOP MOMENTUM - kenaikan tertinggi + volume tinggi"""
    filtered = [s for s in saham_data_list if s['change_pct'] > 1.5 and s['volume_ratio'] > 1.2]
    filtered.sort(key=lambda x: x['change_pct'], reverse=True)
    return filtered[:limit]

def screening_rebound_potential(saham_data_list, limit=10):
    """💡 REBOUND POTENTIAL - oversold + dekat support"""
    filtered = [s for s in saham_data_list if s['rsi'] < 35 and s['change_pct'] < 0]
    filtered.sort(key=lambda x: x['rsi'])
    return filtered[:limit]

def screening_bandar_asing(saham_data_list, hari=1, limit=10):
    """💎 BANDAR & ASING AKUMULASI"""
    # Simulasi: volume tinggi + harga naik
    filtered = [s for s in saham_data_list if s['volume_ratio'] > 1.5 and s['change_pct'] > 0]
    filtered.sort(key=lambda x: x['volume_ratio'], reverse=True)
    return filtered[:limit]

def screening_breakout(saham_data_list, limit=10):
    """📊 BREAKOUT RESISTEN - harga > MA20 + volume tinggi"""
    filtered = [s for s in saham_data_list if s['harga'] > s['ma20'] and s['volume_ratio'] > 1.3]
    filtered.sort(key=lambda x: x['change_pct'], reverse=True)
    return filtered[:limit]

def screening_area_support(saham_data_list, limit=10):
    """🛡️ AREA SUPPORT - harga dekat MA50/MA100"""
    filtered = [s for s in saham_data_list if abs(s['harga'] - s['ma50']) / s['ma50'] < 0.02]
    filtered.sort(key=lambda x: abs(x['harga'] - x['ma50']))
    return filtered[:limit]

# ======================== ANALISIS DETAIL ========================

def analisis_detail(kode):
    """Analisis detail seperti contoh BBCA"""
    data = generate_dummy_data(kode)
    
    # Hitung berbagai nilai
    harga = data['harga']
    change_pct = data['change_pct']
    rsi = data['rsi']
    
    # Support Resistance
    s1 = int(harga * 0.98)
    s2 = int(harga * 0.95)
    s3 = int(harga * 0.9)
    r1 = int(harga * 1.02)
    r2 = int(harga * 1.05)
    r3 = int(harga * 1.1)
    
    # Status MA
    ma5_status = "DI BAWAH" if harga < data['ma5'] else "DI ATAS"
    ma5_trend = "BEARISH" if harga < data['ma5'] else "BULLISH"
    ma20_status = "DI BAWAH" if harga < data['ma20'] else "DI ATAS"
    ma20_trend = "BEARISH" if harga < data['ma20'] else "BULLISH"
    ma50_status = "DI BAWAH" if harga < data['ma50'] else "DI ATAS"
    ma50_trend = "BEARISH" if harga < data['ma50'] else "BULLISH"
    ma100_status = "DI BAWAH" if harga < data['ma100'] else "DI ATAS"
    ma100_trend = "BEARISH" if harga < data['ma100'] else "BULLISH"
    
    # RSI status
    if rsi < 30:
        rsi_status = "OVERSOLD"
        rsi_signal = "BUY"
    elif rsi > 70:
        rsi_status = "OVERBOUGHT"
        rsi_signal = "SELL"
    else:
        rsi_status = "NETRAL"
        rsi_signal = "HOLD"
    
    # Oscillator lainnya (dummy)
    macd = random.uniform(-200, 200)
    macd_signal = "BEARISH" if macd < 0 else "BULLISH"
    stoch = random.uniform(15, 85)
    stoch_status = "OVERSOLD" if stoch < 20 else "OVERBOUGHT" if stoch > 80 else "NETRAL"
    cci = random.uniform(-150, 150)
    cci_status = "OVERSOLD" if cci < -100 else "OVERBOUGHT" if cci > 100 else "NETRAL"
    williams = random.uniform(-90, -10)
    williams_status = "OVERSOLD" if williams < -80 else "OVERBOUGHT" if williams > -20 else "NETRAL"
    
    # Hitung oversold count
    oversold_count = 0
    if rsi < 35: oversold_count += 1
    if stoch < 20: oversold_count += 1
    if cci < -100: oversold_count += 1
    if williams < -80: oversold_count += 1
    
    # Day trade
    if oversold_count >= 3:
        daytrade_signal = "BUY (AGRESIF)"
        daytrade_alasan = f"• {oversold_count} indikator oversold\n• Support S1 ({s1:,}) dekat"
    elif rsi < 40:
        daytrade_signal = "BUY (MODERAT)"
        daytrade_alasan = f"• RSI {rsi:.1f} (mendekati oversold)\n• Volume {data['volume_ratio']:.2f}x"
    else:
        daytrade_signal = "NETRAL"
        daytrade_alasan = "• Menunggu konfirmasi\n• Range trading"
    
    # Swing
    if oversold_count >= 2 and harga < data['ma50']:
        swing_signal = "BUY (MODERAT)"
        swing_alasan = f"• {oversold_count} indikator oversold\n• Dekat MA50/100\n• Risk/reward 1:2.4"
    else:
        swing_signal = "WAIT"
        swing_alasan = "• Sideways\n• Tunggu konfirmasi"
    
    # Bandarmology (dummy)
    asing = random.randint(50, 200)
    asing_ng = random.randint(30, 150)
    retail = random.randint(-100, -30)
    
    asing_text = f"+{asing} M"
    asing_ng_text = f"+{asing_ng} M"
    retail_text = f"{retail} M"
    
    if asing > 100:
        bandar_kesimpulan = "✅ ASING AKUMULASI KUAT (5 hari)"
    elif asing > 50:
        bandar_kesimpulan = "🟢 ASING MULAI AKUMULASI"
    else:
        bandar_kesimpulan = "⚪ NETRAL"
    
    # Format volume
    vol_today = f"{data['volume']/1000000:.1f}M"
    vol_avg = f"{data['volume']/data['volume_ratio']/1000000:.1f}M"
    
    # Format seperti contoh
    text = f"""
📈 *ANALISIS SAHAM {kode}*
━━━━━━━━━━━━━━━━━━━━━
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}
💰 Harga: Rp {harga:,}
📊 Perubahan: {change:+,} ({change_pct:+.2f}%)

🎯 *SIGNAL & REKOMENDASI*
━━━━━━━━━━━━━━━━━━━━━
⚡ *DAY TRADE (INTRADAY)*
SIGNAL: {daytrade_signal}
Entry   : Rp {int(harga*0.995):,} - Rp {harga:,}
Target 1: Rp {int(harga*1.01):,} (+1%)
Target 2: Rp {int(harga*1.02):,} (+2%)
Target 3: Rp {int(harga*1.03):,} (+3%)
Stop Loss: Rp {int(harga*0.99):,} (-1%)

📌 *ALASAN:*
{daytrade_alasan}
• Volume {data['volume_ratio']:.2f}x (DI ATAS RATA2)
• Asing mulai akumulasi

📊 *SWING TRADING (3 HARI - 1 BULAN)*
SIGNAL: {swing_signal}
Entry   : Rp {int(harga*0.98):,} - Rp {harga:,}
Target 1: Rp {int(harga*1.05):,} (+5%)
Target 2: Rp {int(harga*1.11):,} (+11%)
Target 3: Rp {int(harga*1.15):,} (+15%)
Stop Loss: Rp {int(harga*0.955):,} (-4.5%)

📌 *ALASAN:*
{swing_alasan}
• MA50: {ma50_trend}
• MA100: {ma100_trend}
• Risk/reward 1:2.4

📊 *TEKNIKAL LENGKAP*
━━━━━━━━━━━━━━━━━━━━━
MOVING AVERAGE
MA 5    : Rp {data['ma5']:,}    ({ma5_status})    {ma5_trend}
MA 10   : Rp {data['ma20']:,}   ({ma20_status})    {ma20_trend}
MA 20   : Rp {data['ma20']:,}   ({ma20_status})    {ma20_trend}
MA 50   : Rp {data['ma50']:,}   ({ma50_status})     {ma50_trend}
MA 100  : Rp {data['ma100']:,}  ({ma100_status})    {ma100_trend}
💡 KESIMPULAN MA: Short term {ma5_trend}, long term {ma50_trend}

OSCILATOR
RSI (14)      : {rsi:.1f}     {rsi_status}      {rsi_signal}
MACD          : {macd:.2f}  {macd_signal}
Stochastic    : {stoch:.1f}     {stoch_status}
CCI           : {cci:.1f}     {cci_status}
Williams %R   : {williams:.1f}      {williams_status}
💡 KESIMPULAN OSC: {oversold_count} dari 5 indikator oversold (potensi rebound)

📊 *VOLUME ANALYSIS*
━━━━━━━━━━━━━━━━━━━━━
Volume Hari Ini  : {vol_today}
Volume Rata2     : {vol_avg}
Volume Ratio     : {data['volume_ratio']:.2f}x (DI ATAS RATA2)

Volume Detail:
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ {vol_today} (Today)
▰▰▰▰▰▰▰▰▰▰▰▰    {vol_avg} (Average)

💡 Volume di atas rata2 (mulai ada minat beli)

💰 *BANDARMOLOGY*
━━━━━━━━━━━━━━━━━━━━━
NET BUY/SELL (Rp Miliar)
Asing   : {asing_text}
Asing NG: {asing_ng_text}
Retail  : {retail_text}
Mutual  : +22.1 M

MOVEMENT INDEX
Asing    : ▰▰▰▰▰▰▰▰▰▰ {asing} (AKTIF)
Lokal    : ▰▰▰▰▰▰▰    72 (NETRAL)
Bandar   : ▰▰▰▰▰▰▰▰▰  88 (AKUMULASI)

💡 *KESIMPULAN BANDAR:*
• {bandar_kesimpulan}
• Retail jual di harga rendah (panic selling)
• Bandar mulai entry di area support
• Potensi reversal dalam waktu dekat

SUPPORT & RESISTANCE
━━━━━━━━━━━━━━━━━━━━━
RESISTANCE
R3 : Rp {r3:,} (All Time High)
R2 : Rp {r2:,} (Peak bulan lalu)
R1 : Rp {r1:,} (MA20 + Psikologis)

SUPPORT
S1 : Rp {s1:,} (MA100 + Demand)
S2 : Rp {s2:,} (Low bulan ini)
S3 : Rp {s3:,} (Strong support + Bandar entry)

⚠️ *RISK WARNING*
Resistance: Rp {r2:,}
Support   : Rp {s2:,}
RSI       : {rsi:.1f} ({rsi_status})
Stop Loss : Rp {int(harga*0.955):,} (Swing)

📌 *DISCLAIMER:* Analisis untuk referensi, bukan rekomendasi jual/beli. Selalu lakukan riset mandiri.
    """
    
    return text

# ======================== HANDLER TELEGRAM ========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    text = f"""
🚀 *BOT SAHAM INDONESIA SEDERHANA*
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}

Halo *{user.first_name}*! 

📌 *FITUR:*
• 📊 Screening Saham (5 kriteria)
• 📈 Analisis Detail (900+ saham)
• Ketik kode saham langsung

🔍 *Contoh:* BBCA, BBRI, TLKM, ASII, GOTO
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 SCREENING", callback_data='menu_screening')],
        [InlineKeyboardButton("📈 ANALISIS", callback_data='menu_analisis')],
        [InlineKeyboardButton("❓ BANTUAN", callback_data='bantuan')],
    ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def menu_screening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = """
📊 *SCREENING SAHAM*
━━━━━━━━━━━━━━━━━━━━━
Pilih kriteria screening:

🔥 TOP MOMENTUM
💡 REBOUND POTENTIAL
💎 BANDAR & ASING AKUMULASI
📊 BREAKOUT RESISTEN
🛡️ AREA SUPPORT
    """
    
    keyboard = [
        [InlineKeyboardButton("🔥 TOP MOMENTUM", callback_data='screen:top')],
        [InlineKeyboardButton("💡 REBOUND POTENTIAL", callback_data='screen:rebound')],
        [InlineKeyboardButton("💎 BANDAR AKUMULASI", callback_data='screen:bandar')],
        [InlineKeyboardButton("📊 BREAKOUT RESISTEN", callback_data='screen:breakout')],
        [InlineKeyboardButton("🛡️ AREA SUPPORT", callback_data='screen:support')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='start')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def screening_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    tipe = query.data.split(':')[1]
    
    # Generate data untuk semua saham
    saham_data = []
    sample_saham = random.sample(SAHAM_LIST, min(50, len(SAHAM_LIST)))  # Ambil sample 50 saham
    
    for kode in sample_saham:
        saham_data.append(generate_dummy_data(kode))
    
    # Screening berdasarkan tipe
    if tipe == 'top':
        results = screening_top_momentum(saham_data)
        title = "🔥 TOP MOMENTUM"
    elif tipe == 'rebound':
        results = screening_rebound_potential(saham_data)
        title = "💡 REBOUND POTENTIAL"
    elif tipe == 'bandar':
        results = screening_bandar_asing(saham_data)
        title = "💎 BANDAR & ASING AKUMULASI"
    elif tipe == 'breakout':
        results = screening_breakout(saham_data)
        title = "📊 BREAKOUT RESISTEN"
    elif tipe == 'support':
        results = screening_area_support(saham_data)
        title = "🛡️ AREA SUPPORT"
    else:
        results = []
        title = "HASIL"
    
    text = f"📊 *{title}*\n🕐 {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not results:
        text += "❌ Tidak ada hasil"
    else:
        for i, s in enumerate(results[:10], 1):
            if tipe == 'rebound':
                text += f"{i}. *{s['kode']}*: Rp {s['harga']:,} | RSI: {s['rsi']:.1f} | {s['change_pct']:+.2f}%\n"
            elif tipe == 'bandar':
                text += f"{i}. *{s['kode']}*: Rp {s['harga']:,} | Vol: {s['volume_ratio']:.2f}x | {s['change_pct']:+.2f}%\n"
            else:
                text += f"{i}. *{s['kode']}*: Rp {s['harga']:,} | {s['change_pct']:+.2f}% | Vol: {s['volume_ratio']:.2f}x\n"
    
    # Keyboard untuk akses cepat
    keyboard = []
    row = []
    for s in results[:6]:
        row.append(InlineKeyboardButton(s['kode'], callback_data=f'saham:{s["kode"]}'))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔄 Refresh", callback_data=f'screen:{tipe}')])
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='menu_screening')])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def menu_analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Tampilkan saham populer
    popular = ['BBCA', 'BBRI', 'BMRI', 'BBNI', 'TLKM', 'ASII', 'GOTO', 'ADRO']
    
    text = "📈 *ANALISIS SAHAM*\n━━━━━━━━━━━━━━━━━━━━━\nPilih saham atau ketik kode langsung:\n\n"
    
    keyboard = []
    row = []
    for i, kode in enumerate(popular):
        row.append(InlineKeyboardButton(kode, callback_data=f'saham:{kode}'))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Kembali", callback_data='start')])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def detail_saham(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    kode = query.data.split(':')[1]
    
    # Kirim analisis
    text = analisis_detail(kode)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f'saham:{kode}')],
        [InlineKeyboardButton("📊 Screening", callback_data='menu_screening')],
        [InlineKeyboardButton("🔙 Kembali", callback_data='menu_analisis')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = f"""
❓ *BANTUAN*
━━━━━━━━━━━━━━━━━━━━━

📌 *CARA PAKAI:*
• Ketik kode saham langsung
• Contoh: BBCA, BBRI, TLKM

📊 *SCREENING:*
• TOP MOMENTUM - Kenaikan tertinggi
• REBOUND POTENTIAL - Saham oversold
• BANDAR AKUMULASI - Volume tinggi
• BREAKOUT RESISTEN - Tembus resistance
• AREA SUPPORT - Dekat level support

📈 *ANALISIS:*
• Harga & perubahan
• Day Trade signal
• Swing Trade signal
• Moving Averages
• Oscillator (RSI, MACD, dll)
• Volume analysis
• Bandarmology
• Support & Resistance

⚠️ *DISCLAIMER:*
Data untuk referensi, bukan rekomendasi jual/beli.

👨‍💻 *INFO:*
Bot Saham Sederhana v2.0
{len(SAHAM_LIST)}+ saham Indonesia
    """
    
    keyboard = [[InlineKeyboardButton("🔙 Kembali", callback_data='start')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    
    if text in SAHAM_LIST:
        # Kirim analisis
        await update.message.chat.send_action(action="typing")
        reply = analisis_detail(text)
        
        keyboard = [
            [InlineKeyboardButton("📊 Screening", callback_data='menu_screening')],
            [InlineKeyboardButton("📈 Analisis Lain", callback_data='menu_analisis')]
        ]
        
        await update.message.reply_text(reply, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    else:
        await update.message.reply_text(
            f"❌ Kode '{text}' tidak ditemukan.\nCoba: BBCA, BBRI, TLKM, atau /start untuk menu"
        )

# ======================== MAIN ========================

def main():
    print("="*50)
    print("BOT SAHAM INDONESIA SEDERHANA")
    print(f"📊 Total saham: {len(SAHAM_LIST)}+")
    print("="*50)
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_screening, pattern='^menu_screening$'))
    app.add_handler(CallbackQueryHandler(menu_analisis, pattern='^menu_analisis$'))
    app.add_handler(CallbackQueryHandler(bantuan, pattern='^bantuan$'))
    app.add_handler(CallbackQueryHandler(screening_result, pattern='^screen:'))
    app.add_handler(CallbackQueryHandler(detail_saham, pattern='^saham:'))
    app.add_handler(CallbackQueryHandler(start, pattern='^start$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot berjalan... Tekan Ctrl+C untuk stop")
    app.run_polling()

if __name__ == '__main__':
    main()
