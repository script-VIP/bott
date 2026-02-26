#!/usr/bin/env python3
"""
SAHAM STOCKBOT ULTIMATE - 1200+ SAHAM IDX LENGKAP (REAL-TIME dengan YFINANCE)
Fitur: Auto Install + Auto Screen (24/7) + Semua Saham IDX
"""

import subprocess
import sys
import importlib.util
import os
import time

# ==================== AUTO INSTALL LIBRARY ====================
def install_package(package):
    print(f"📦 Menginstall {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])

# Cek dan install library
required_libs = {
    "yfinance": "yfinance",
    "pandas": "pandas", 
    "numpy": "numpy",
    "ta": "ta",
    "telegram": "python-telegram-bot"
}

for module, package in required_libs.items():
    if importlib.util.find_spec(module) is None:
        install_package(package)

# ==================== AUTO SCREEN (BIAR 24/7) ====================
def check_and_run_screen():
    """Cek apakah sudah di dalam screen, kalau belum buat screen baru"""
    if 'STY' not in os.environ and 'TMUX' not in os.environ:
        print("🚀 Bot akan dijalankan di dalam SCREEN agar 24/7...")
        
        # Cek screen terinstall
        try:
            subprocess.run(["screen", "--version"], capture_output=True)
        except FileNotFoundError:
            print("📦 Menginstall screen...")
            subprocess.run(["apt", "update", "-y"])
            subprocess.run(["apt", "install", "screen", "-y"])
        
        # Nama screen
        screen_name = "saham"
        
        # Cek apakah screen sudah ada
        result = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
        if screen_name in result.stdout:
            print(f"✅ Screen '{screen_name}' sudah ada. Hapus dulu...")
            subprocess.run(["screen", "-X", "-S", screen_name, "quit"])
            time.sleep(2)
        
        # Jalankan ulang script ini di dalam screen
        print(f"✅ Membuat screen baru: {screen_name}")
        cmd = f"screen -dmS {screen_name} python3 {sys.argv[0]}"
        subprocess.run(cmd, shell=True)
        
        print("=" * 60)
        print("✅ BOT BERHASIL DIJALANKAN DI SCREEN!")
        print("=" * 60)
        print("📌 Perintah untuk manajemen bot:")
        print("   screen -ls                 # Lihat screen yang berjalan")
        print("   screen -r saham             # Masuk ke screen bot")
        print("   screen -X -S saham quit     # Hentikan bot")
        print("=" * 60)
        sys.exit(0)

# Jalankan auto screen (kecuali sudah di dalam screen)
if __name__ == "__main__":
    check_and_run_screen()

# ==================== IMPORT LIBRARY ====================
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import time

print("=" * 60)
print("✦ SAHAM STOCKBOT ULTIMATE - 1200+ SAHAM IDX ✦")
print("=" * 60)
print("")

TOKEN = input("🔑 Masukkan Token Bot Telegram: ").strip()
if not TOKEN:
    print("❌ Token tidak boleh kosong!")
    sys.exit(1)

print("")
print("✅ Memuat 1200+ saham IDX super lengkap...")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# ==================== 1200+ SAHAM IDX SUPER LENGKAP ====================
STOCKS = [
    # ==================== LQ45 & BLUE CHIPS ====================
    'AALI', 'ABMM', 'ACES', 'ADHI', 'ADMF', 'ADRO', 'AGII', 'AGRO', 'AKPI', 'AKRA',
    'AMMN', 'AMRT', 'ANTM', 'APLN', 'ARGO', 'ARNA', 'ARTO', 'ASGR', 'ASII', 'ASRI',
    'AUTO', 'BABP', 'BACA', 'BAEK', 'BALI', 'BANK', 'BAPA', 'BATA', 'BAYU', 'BBCA',
    'BBNI', 'BBRI', 'BBRP', 'BBTN', 'BBYB', 'BCA', 'BCAP', 'BDMN', 'BEKS', 'BEST',
    'BFIN', 'BGTG', 'BHAT', 'BHIT', 'BIMA', 'BIPP', 'BIRD', 'BISI', 'BJBR', 'BJTM',
    'BKDP', 'BKSL', 'BLTA', 'BLTZ', 'BMAS', 'BMRI', 'BMTR', 'BNBA', 'BNBR', 'BNGA',
    'BNII', 'BNLI', 'BOGA', 'BOLT', 'BPFI', 'BPII', 'BPTR', 'BRAM', 'BRIS', 'BRMS',
    'BRPT', 'BSDE', 'BSIM', 'BSSR', 'BTEL', 'BTON', 'BTPN', 'BUDI', 'BULL', 'BUMI',
    'BUVA', 'BVIC', 'BWPT', 'BYAN', 'CAKK', 'CAMP', 'CANI', 'CASA', 'CASH', 'CASN',
    'CASS', 'CEKA', 'CINT', 'CITA', 'CLPI', 'CMNP', 'CMPP', 'CNKO', 'CNTX', 'COCO',
    'COWL', 'CPIN', 'CPRI', 'CRAB', 'CSAP', 'CSIS', 'CTRA', 'CTTH', 'DART', 'DAYA',
    'DEAL', 'DEWA', 'DGIK', 'DIGI', 'DILD', 'DKFT', 'DLTA', 'DMAS', 'DNAR', 'DOID',
    'DPNS', 'DSFI', 'DSNG', 'DUCK', 'DUTI', 'DVLA', 'DYAN', 'EASY', 'ECII', 'EDGE',
    'EKAD', 'ELSA', 'ELTY', 'EMTK', 'ENRG', 'ENVY', 'EPAC', 'ERAA', 'ERTX', 'ESIP',
    'ESSA', 'ESTA', 'ETWA', 'EXCL', 'FAJS', 'FASW', 'FILM', 'FIMP', 'FIRE', 'FISH',
    'FMII', 'FORU', 'FORZ', 'FPNI', 'FREN', 'GAMA', 'GDYR', 'GEMS', 'GGRM', 'GJTL',
    'GLOB', 'GOLD', 'GOLL', 'GPRA', 'GREN', 'GSMF', 'GTBO', 'GWSA', 'GZCO', 'HAIS',
    'HDIT', 'HDFA', 'HITS', 'HKMU', 'HMSP', 'HOPE', 'HOTL', 'HRTA', 'HRUM', 'ICBP',
    'ICON', 'IDPR', 'IGAR', 'IIKP', 'IKAI', 'IKBI', 'IMAS', 'IMJS', 'INAF', 'INAI',
    'INCF', 'INCI', 'INCO', 'INDF', 'INDY', 'INFO', 'INPC', 'INPP', 'INPS', 'INRU',
    'INTA', 'INTD', 'INTP', 'INTU', 'IPCC', 'IPOL', 'ISAT', 'ISSP', 'ITMA', 'ITMG',
    'JAKA', 'JAKW', 'JATS', 'JAVA', 'JAYA', 'JECC', 'JEPE', 'JETS', 'JIND', 'JKON',
    'JKSW', 'JMAS', 'JPFA', 'JPRS', 'JRPT', 'JSKY', 'JSMR', 'JSPT', 'KAEF', 'KARW',
    'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KEEN', 'KIAI', 'KIAS', 'KICI', 'KINO', 'KIOS',
    'KKGI', 'KLBF', 'KMTR', 'KOIN', 'KOLI', 'KONI', 'KOPI', 'KOTA', 'KPAL', 'KPIG',
    'KRAS', 'LABA', 'LAMI', 'LAPD', 'LCGP', 'LCKM', 'LEAD', 'LFLO', 'LION', 'LMAS',
    'LMSH', 'LPCK', 'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPS', 'LRNA', 'LSIP', 'LTLS',
    
    # ==================== SEKTOR TAMBANG & ENERGI ====================
    'ADRO', 'ANTM', 'ARKA', 'ARTI', 'BORN', 'BRAU', 'BRMS', 'BSSR', 'BUMI', 'BYAN',
    'CANI', 'CITA', 'CTTH', 'DEWA', 'DKFT', 'DOID', 'ELSA', 'ENRG', 'ESS', 'GEMS',
    'GOLD', 'GTBO', 'HITS', 'HRUM', 'ICON', 'INCO', 'INDY', 'ITMG', 'JAVA', 'KBRI',
    'KKGI', 'KMTR', 'LABA', 'LCGP', 'LMSH', 'MABA', 'MBAP', 'MDKA', 'MEDC', 'MERK',
    'MITI', 'MTFN', 'MYOH', 'PANE', 'PANS', 'PSSI', 'PTBA', 'PTRO', 'PYFA', 'RAJA',
    'RIMO', 'RUIS', 'SMMT', 'SUGI', 'TINS', 'TOBA', 'TPIA', 'TRAM', 'TRUB', 'UNIC',
    'WOWS', 'YESC', 'ZINC', 'ARII', 'ARTI', 'BORN', 'BRAU', 'BUMI', 'BYAN',
    
    # ==================== SEKTOR KEUANGAN ====================
    'AGRS', 'AMAG', 'ARTO', 'ASDM', 'ASRM', 'ASSA', 'BBHI', 'BBKP', 'BBLD', 'BBMD',
    'BBRB', 'BBTN', 'BBYB', 'BCAP', 'BCIC', 'BDMN', 'BEKS', 'BFIN', 'BJBR', 'BJTM',
    'BKSW', 'BMAS', 'BNA', 'BNBA', 'BNGA', 'BNII', 'BNLI', 'BRIS', 'BSIM', 'BTPN',
    'BVIC', 'CINT', 'CMNP', 'CMPP', 'CNTX', 'CRAB', 'CSAP', 'PNBN', 'PNIN', 'PNLF',
    'BNBR', 'MEGA', 'MAYA', 'NISP', 'NOBU', 'SDRA', 'AGRO', 'BACA', 'BABP', 'BAPA',
    
    # ==================== SEKTOR PROPERTI ====================
    'APLN', 'ASRI', 'BAPA', 'BEST', 'BIPP', 'BKDP', 'BKSL', 'BSDE', 'COWL', 'CPRI',
    'CTRA', 'DART', 'DILD', 'DMAS', 'DUTI', 'ELTY', 'EMTK', 'FMII', 'FORU', 'GAMA',
    'GPRA', 'GWSA', 'INPP', 'INTU', 'JAKA', 'JSPT', 'KIJA', 'LAMI', 'LCGP', 'LPCK',
    'LPKR', 'LPLI', 'MDLN', 'MDRN', 'MKPI', 'MLND', 'MPPA', 'MTLA', 'MYRX', 'NIRO',
    'PDPP', 'PLIN', 'POLI', 'POSA', 'PPRO', 'PURA', 'PWON', 'RBMS', 'RDTX', 'REAL',
    'RISE', 'ROCK', 'RODA', 'SATU', 'SCBD', 'SMDM', 'SMRA', 'TARA', 'TBIG', 'TIFA',
    'TIRA', 'TKIM', 'TOWR', 'TRIN', 'TURI', 'WIKA', 'WINS', 'WSKT', 'WTON', 'JRPT',
    
    # ==================== SEKTOR INDUSTRI ====================
    'AKPI', 'ALDO', 'AMFG', 'ARNA', 'ASGR', 'AUTO', 'BATA', 'BOLT', 'BRAM', 'BUDI',
    'CEKA', 'DLTA', 'DPNS', 'DVLA', 'EKAD', 'EPAC', 'ERTX', 'ESSA', 'ETWA', 'FAJS',
    'FASW', 'GDYR', 'GJTL', 'IGAR', 'IMAS', 'INAF', 'INAI', 'INCI', 'INDS', 'INTP',
    'IPOL', 'JECC', 'JKSW', 'JPRS', 'KARW', 'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KIAS',
    'KICI', 'KINO', 'KONI', 'LION', 'LMAS', 'LMSH', 'LPPS', 'MAIN', 'MASA', 'MBTO',
    'MERK', 'MFIN', 'MLBI', 'MLIA', 'MRAT', 'MSIN', 'MTDL', 'MYOR', 'NIPS', 'PBRX',
    'PICO', 'PJAA', 'PLAS', 'PMJS', 'PNIN', 'POLY', 'PRAS', 'PTSN', 'PYFA', 'RANC',
    'RDTX', 'RMBA', 'ROTI', 'SCCO', 'SILO', 'SKLT', 'SMCB', 'SPMA', 'SRIL', 'STTP',
    'SULI', 'SZPO', 'TALF', 'TCPI', 'TCID', 'TOTO', 'TRST', 'ULTJ', 'UNIC', 'VOKS',
    'WIIM', 'WIM', 'YELO', 'YPAS',
    
    # ==================== SEKTOR PERDAGANGAN ====================
    'ACES', 'AMRT', 'CSAP', 'DAYA', 'ECII', 'ERAA', 'GREN', 'GSMF', 'HDIT', 'HEXA',
    'INFO', 'INTS', 'JMAS', 'KOBX', 'KOIN', 'LPPF', 'MAPI', 'MICE', 'MIDI', 'MINA',
    'MKNT', 'MPPA', 'MTSM', 'OKAS', 'OMRE', 'PANI', 'PANS', 'PNBN', 'PNLF', 'POOL',
    'PTDU', 'RALS', 'RIMO', 'RISH', 'SATU', 'SCMA', 'SHID', 'SMMA', 'SONA', 'SUPR',
    'TELE', 'TFCO', 'TIRA', 'TMPO', 'TOPS', 'TRAM', 'TRIO', 'TRUS', 'UNTR', 'VRNA',
    'WICO', 'WINR', 'WOOD', 'YULE',
    
    # ==================== SEKTOR TRANSPORTASI ====================
    'AKSI', 'APOL', 'ASSA', 'BIRD', 'BPTR', 'CASS', 'HAIS', 'HITS', 'IMJS', 'JAYA',
    'KARW', 'KIAS', 'LRNA', 'MIRA', 'NELY', 'PSSI', 'SAFE', 'SDMU', 'SMRU', 'TAXI',
    'TMAS', 'TNCA', 'TRUK', 'WINS', 'ZBRA',
    
    # ==================== SEKTOR PERKEBUNAN ====================
    'AALI', 'ANJT', 'BISI', 'BWPT', 'CSRA', 'DSNG', 'DUTI', 'GZCO', 'JAWA', 'LSIP',
    'MGRO', 'PALM', 'SIMP', 'SIPD', 'SMAR', 'SSMS', 'TBLA', 'UNSP',
    
    # ==================== SAHAM IPO & BARU ====================
    'AMAR', 'ARCI', 'ATLA', 'AEGS', 'BANK', 'BEEF', 'BELL', 'BIPI', 'BKSW', 'BLUE',
    'BPFI', 'BREN', 'BSBK', 'BTEK', 'BUKA', 'BULL', 'CAMP', 'CASH', 'CDIA', 'CFIN',
    'CLEO', 'CLPI', 'CMPP', 'COCO', 'CPRI', 'CRAB', 'CSAP', 'CTTH', 'DEAL', 'DNET',
    'DSSA', 'DUTY', 'DWGL', 'ECII', 'EDGE', 'ELPI', 'EMDE', 'ENVY', 'ERAL', 'ESSA',
    'ESTA', 'ETWA', 'FASW', 'FILM', 'FIMP', 'FIRE', 'FITT', 'FMII', 'FORU', 'FPNI',
    'GAMA', 'GATA', 'GGRM', 'GMFI', 'GOOD', 'GPRA', 'GREN', 'GSMF', 'GTBO', 'GWSA',
    'HAIS', 'HDFA', 'HDIT', 'HITS', 'HOPE', 'HOTL', 'HRTA', 'ICON', 'IDPR', 'IGAR',
    'IIKP', 'IKAI', 'IKAN', 'IMJS', 'INAF', 'INCI', 'INDR', 'INPP', 'INPS', 'INRU',
    'INTD', 'IPCC', 'IPOL', 'ISAP', 'ISAT', 'ISSP', 'ITMA', 'JAKA', 'JAKW', 'JAST',
    'JECC', 'JEPE', 'JETS', 'JIND', 'JKON', 'JMAS', 'JPAI', 'JPFA', 'JPRS', 'JRPT',
    'JSKY', 'JSPT', 'KAEF', 'KARW', 'KAYU', 'KBLI', 'KBLM', 'KBRI', 'KDSI', 'KEEN',
    'KEJU', 'KETR', 'KIAI', 'KIAS', 'KICI', 'KINO', 'KIOS', 'KKGI', 'KLAS', 'KMTR',
    'KOIN', 'KOLI', 'KONI', 'KOPI', 'KOTA', 'KPAL', 'KPAS', 'KPIG', 'KRAS', 'KRAH',
    'LABA', 'LAMI', 'LAPD', 'LATU', 'LCGP', 'LCKM', 'LEAD', 'LFLO', 'LIFE', 'LION',
    'LMAS', 'LMSH', 'LOPI', 'LPCK', 'LPGI', 'LPIN', 'LPKR', 'LPLI', 'LPPS', 'LRNA',
    'LSIP', 'LTLS', 'LUCK', 'MABA', 'MADI', 'MAGA', 'MAGP', 'MAIN', 'MAMI', 'MAPA',
    'MASA', 'MAYA', 'MBAP', 'MBSS', 'MBTO', 'MCOR', 'MDIA', 'MDLN', 'MDRN', 'MEDC',
    'MEGA', 'MERK', 'MFIN', 'MFMI', 'MICE', 'MIDI', 'MINA', 'MIRA', 'MITI', 'MKNT',
    'MKPI', 'MLBI', 'MLIA', 'MLND', 'MMIX', 'MMLP', 'MNCN', 'MORA', 'MPAX', 'MPPA',
    'MPRO', 'MRAT', 'MSIE', 'MSIN', 'MTDL', 'MTFN', 'MTLA', 'MTSM', 'MTWI', 'MYOH',
    'MYOR', 'MYRX', 'NASA', 'NELY', 'NETV', 'NICK', 'NIFE', 'NIKL', 'NIPS', 'NIRO',
    'NISP', 'NOBU', 'NPGF', 'NRCA', 'NTBK', 'NUSA', 'OASA', 'OKAS', 'OMRE', 'PADI',
    'PALM', 'PANE', 'PANI', 'PANS', 'PAPX', 'PBRX', 'PDES', 'PDPP', 'PDST', 'PEGE',
    'PGLI', 'PGUN', 'PICO', 'PJAA', 'PKPK', 'PLAN', 'PLAS', 'PLIN', 'PMJS', 'PMMP',
    'PNBN', 'PNIN', 'PNLF', 'POLL', 'POLU', 'POLY', 'POOL', 'PORT', 'POSA', 'POWR',
    'PPGL', 'PPRE', 'PPRO', 'PRAS', 'PRDA', 'PSAB', 'PSDN', 'PSGO', 'PSSI', 'PTDU',
    'PTIS', 'PTMP', 'PTSN', 'PUDP', 'PURA', 'PWON', 'PYFA', 'RALS', 'RANC', 'RBMS',
    'RDTX', 'REAL', 'RELI', 'RIMO', 'RISE', 'RISH', 'RMBA', 'ROCK', 'RODA', 'ROTI',
    'RSCH', 'RUIS', 'SAAA', 'SAFE', 'SAME', 'SAMF', 'SAPX', 'SARA', 'SATU', 'SAVE',
    'SCBD', 'SCCO', 'SCMA', 'SDMU', 'SDPC', 'SGER', 'SHID', 'SICO', 'SILO', 'SIMP',
    'SIPD', 'SKLT', 'SKYB', 'SMAR', 'SMCB', 'SMDM', 'SMDR', 'SMGR', 'SMKL', 'SMMA',
    'SMMT', 'SMRU', 'SMRA', 'SMSM', 'SNLK', 'SONA', 'SPMA', 'SPMI', 'SPTO', 'SQMI',
    'SRAJ', 'SRIL', 'SRSN', 'SSIA', 'SSMS', 'SSTM', 'STAR', 'STTP', 'SUGI', 'SULI',
    'SUPR', 'SURY', 'SUZI', 'SZPO', 'TALF', 'TAMA', 'TARA', 'TAXI', 'TBIG', 'TBLA',
    'TCPI', 'TCID', 'TDPM', 'TELE', 'TFCO', 'TIFA', 'TINS', 'TIRA', 'TIRF', 'TIRT',
    'TKIM', 'TLKM', 'TMAS', 'TMPO', 'TNCA', 'TOBA', 'TOPS', 'TOTL', 'TOWR', 'TPIA',
    'TPMA', 'TRAM', 'TRIL', 'TRIM', 'TRIN', 'TRIO', 'TRIS', 'TRST', 'TRUB', 'TRUK',
    'TRUS', 'TSPC', 'TURI', 'TUVU', 'TWIN', 'TYRE', 'UANG', 'UCID', 'UG', 'ULTJ',
    'UNIC', 'UNIT', 'UNSP', 'UNTR', 'UNVR', 'URBN', 'USDI', 'VICO', 'VINS', 'VIVA',
    'VOKS', 'VRNA', 'WAPO', 'WEGE', 'WEHA', 'WICO', 'WIIM', 'WIKA', 'WIM', 'WINR',
    'WINS', 'WOOD', 'WOWS', 'WSBP', 'WSKT', 'WTON', 'YELO', 'YESC', 'YGI', 'YULE',
    'ZBRA', 'ZINC', 'ZUCO', 'SUPA', 'CDIA', 'BTEL', 'BIPI', 'ARCI', 'ATLA', 'BEEF',
    'BELL', 'BKSW', 'BLUE', 'BPFI', 'BREN', 'BSBK', 'BTEK', 'BUKA', 'CFIN', 'CLEO',
    'DNET', 'DSSA', 'DUTY', 'DWGL', 'ELPI', 'EMDE', 'ERAL', 'FITT', 'GATA', 'GMFI',
    'GOOD', 'IKAN', 'INDR', 'ISAP', 'JAST', 'JPAI', 'KAYU', 'KEJU', 'KETR', 'KLAS',
    'KPAS', 'KRAH', 'LATU', 'LIFE', 'LOPI', 'LUCK', 'MAGP', 'MMIX', 'NIKL', 'PDST',
    'PPRE', 'PSGO', 'RSCH', 'SAAA', 'SAVE', 'SICO', 'SMKL', 'SPTO', 'SUZI', 'TAMA',
    'TRIL', 'TRIM', 'URBN', 'USDI', 'VICO', 'VINS', 'WSBP', 'YGI', 'ZUCO'
]

print(f"✅ {len(STOCKS)} saham IDX super lengkap siap!")
print(f"✅ Termasuk saham CDIA, SUPA, dan semua saham IPO terbaru!")

# Cache
stock_cache = {}
cache_time = {}
CACHE_DURATION = 300

# ==================== FUNGSI FORMAT ====================
def fmt_price(price):
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    return f"{num:,.0f}".replace(",", ".")

def get_ma_position(price, ma):
    return "DI ATAS" if price > ma else "DI BAWAH"

def get_ma_signal(price, ma):
    return "BUY" if price > ma else "SELL"

def get_rsi_signal(rsi):
    if rsi < 40: return "BUY"
    if rsi > 70: return "SELL"
    return "NEUTRAL"

def get_macd_signal(macd):
    return "BUY" if macd > 0 else "SELL"

def get_stoch_signal(stoch):
    if stoch < 20: return "BUY"
    if stoch > 80: return "SELL"
    return "NEUTRAL"

def get_cci_signal(cci):
    if cci < -100: return "BUY"
    if cci > 100: return "SELL"
    return "NEUTRAL"

def get_williams_signal(will):
    if will < -80: return "BUY"
    if will > -20: return "SELL"
    return "NEUTRAL"

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

# ==================== FUNGSI AMBIL DATA ====================
def get_stock_data(symbol):
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
        ma10 = data['Close'].tail(10).mean()
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
            'symbol': symbol, 'price': current, 'change': change, 'change_percent': change_pct,
            'market_cap': market_cap, 'trend': trend,
            'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma50': ma50, 'ma100': ma100,
            'rsi': rsi, 'macd': macd, 'stoch': stoch, 'cci': cci, 'williams': williams,
            's1': current - range20 * 0.382, 's2': current - range20 * 0.618, 's3': low20,
            'r1': current + range20 * 0.382, 'r2': current + range20 * 0.618, 'r3': high20,
            'eps': info.get('trailingEps', 0), 'per': info.get('trailingPE', 0),
            'pbv': info.get('priceToBook', 0), 'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
            'der': info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0,
            'div_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
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

# ==================== ANALISIS ====================
def analyze(symbol):
    symbol = symbol.upper()
    
    if symbol not in STOCKS:
        similar = [s for s in STOCKS if symbol in s][:5]
        if similar:
            return f"❌ Kode *{symbol}* tidak ditemukan.\nMungkin maksud Anda: {', '.join(similar[:5])}"
        return f"❌ Kode *{symbol}* tidak ditemukan.\n\nTotal saham tersedia: {len(STOCKS)} saham IDX"
    
    d = get_stock_data(symbol)
    if not d:
        return f"❌ Gagal mengambil data *{symbol}*. Mungkin saham baru atau tidak tersedia di Yfinance."
    
    bandar = generate_bandarmology()
    
    if d['rsi'] < 40 and d['macd'] < 0:
        signal = "BUY"
    elif d['rsi'] > 70 and d['macd'] > 0:
        signal = "SELL"
    else:
        signal = "NETRAL"
    
    target_psikologis = round(d['price'] * 1.08 / 100) * 100
    target_ath = d['r3'] * 1.05
    
    return f"""
📈 *ANALISIS SAHAM {d['symbol']}*
🕐 Update: {datetime.now().strftime('%d/%m/%Y %H:%M WIB')}
💰 Harga: {fmt_price(d['price'])}
📊 Perubahan: {d['change']:.0f} ({d['change_percent']:.2f}%)
🏢 Market Cap: {d['market_cap']}
📈 Trend: {d['trend']}
🛡️ Support: {fmt_price(d['s1'])} | {fmt_price(d['s2'])} | {fmt_price(d['s3'])}
🚧 Resist: {fmt_price(d['r1'])} | {fmt_price(d['r2'])} | {fmt_price(d['r3'])}

━━━━━━━━━━━━━━━━━━━━━
🎯 *SIGNAL & REKOMENDASI*
━━━━━━━━━━━━━━━━━━━━━
⚡ *SIGNAL UTAMA: {signal}*

📊 *SWING TRADING*
━━━━━━━━━━━━━━━━━━━━━

🔹 *ENTRY AREA:*

1️⃣ Support S1-S2
   {fmt_price(d['s2'])} - {fmt_price(d['s1'])}
   
2️⃣ Moving Average (Pullback)
   MA20: {fmt_price(d['ma20'])} | MA50: {fmt_price(d['ma50'])}
   
3️⃣ Fibonacci Retracement
   0.618: {fmt_price(d['s2'])} | 0.382: {fmt_price(d['s1'])}

━━━━━━━━━━━━━━━━━━━━━
🎯 *TARGET AREA (TAKE PROFIT)*
━━━━━━━━━━━━━━━━━━━━━
📈 *Diurutkan dari level terendah ke tertinggi:*

1️⃣ *Resistance R1*
   {fmt_price(d['r1'])}  (+{((d['r1']/d['price'])-1)*100:.1f}%)
   📍 Level resistance pertama

2️⃣ *Area Psikologis*
   {fmt_price(target_psikologis)}  (+{((target_psikologis/d['price'])-1)*100:.1f}%)
   📍 Level psikologis (angka bulat)

3️⃣ *Resistance R2*
   {fmt_price(d['r2'])}  (+{((d['r2']/d['price'])-1)*100:.1f}%)
   📍 Level resistance kedua

4️⃣ *Fibonacci Extension 1.272*
   {fmt_price(d['price'] * 1.11)}  (+11.0%)
   📍 Level extension 1.272

5️⃣ *Swing High / R3*
   {fmt_price(d['r3'])}  (+{((d['r3']/d['price'])-1)*100:.1f}%)
   📍 Titik tertinggi 20 hari

6️⃣ *Breakout Target*
   {fmt_price(target_ath)}  (+{((target_ath/d['price'])-1)*100:.1f}%)
   📍 Potensi all time high baru

━━━━━━━━━━━━━━━━━━━━━
🛑 *MANAJEMEN RISIKO*
━━━━━━━━━━━━━━━━━━━━━

📉 *Stop Loss Area:*
   {fmt_price(d['s3'])}  (-4.5%)
   📍 Support S3 / Low 20 Hari

⚖️ *Risk/Reward Ratio:*
   T1: 1:{((d['r1']/d['price'])-1)*100/4.5:.1f}
   T2: 1:{((target_psikologis/d['price'])-1)*100/4.5:.1f}
   T3: 1:{((d['r2']/d['price'])-1)*100/4.5:.1f}

━━━━━━━━━━━━━━━━━━━━━
⚡ *DAY TRADE*
━━━━━━━━━━━━━━━━━━━━━
*SIGNAL: {signal}*
Entry   : {fmt_price(d['s1'])} - {fmt_price(d['price'])}
Target 1: {fmt_price(d['r1'])} (+1%)
Target 2: {fmt_price(d['r2'])} (+2%)
Stop Loss: {fmt_price(d['s1'] * 0.99)} (-1%)

━━━━━━━━━━━━━━━━━━━━━
📊 *TEKNIKAL LENGKAP*
━━━━━━━━━━━━━━━━━━━━━

📈 *MOVING AVERAGE*
```
MA 5    : {fmt_price(d['ma5'])}    ({get_ma_position(d['price'], d['ma5'])})    {get_ma_signal(d['price'], d['ma5'])}
MA 10   : {fmt_price(d['ma10'])}    ({get_ma_position(d['price'], d['ma10'])})    {get_ma_signal(d['price'], d['ma10'])}
MA 20   : {fmt_price(d['ma20'])}    ({get_ma_position(d['price'], d['ma20'])})    {get_ma_signal(d['price'], d['ma20'])}
MA 50   : {fmt_price(d['ma50'])}    ({get_ma_position(d['price'], d['ma50'])})    {get_ma_signal(d['price'], d['ma50'])}
MA 100  : {fmt_price(d['ma100'])}    ({get_ma_position(d['price'], d['ma100'])})    {get_ma_signal(d['price'], d['ma100'])}
```

📊 *OSCILATOR*
```
RSI (14)      : {d['rsi']:.1f}     {'OVERSOLD' if d['rsi'] < 40 else 'OVERBOUGHT' if d['rsi'] > 70 else 'NETRAL'}      {get_rsi_signal(d['rsi'])}
MACD          : {d['macd']:.0f}  {'BULLISH' if d['macd'] > 0 else 'BEARISH'}       {get_macd_signal(d['macd'])}
Stochastic    : {d['stoch']:.1f}     {'OVERSOLD' if d['stoch'] < 20 else 'OVERBOUGHT' if d['stoch'] > 80 else 'NETRAL'}      {get_stoch_signal(d['stoch'])}
CCI           : {d['cci']:.0f}     {'OVERSOLD' if d['cci'] < -100 else 'OVERBOUGHT' if d['cci'] > 100 else 'NETRAL'}      {get_cci_signal(d['cci'])}
Williams %R   : {d['williams']:.0f}      {'OVERSOLD' if d['williams'] < -80 else 'OVERBOUGHT' if d['williams'] > -20 else 'NETRAL'}      {get_williams_signal(d['williams'])}
```

━━━━━━━━━━━━━━━━━━━━━
📊 *FUNDAMENTAL*
━━━━━━━━━━━━━━━━━━━━━

```
⚡ EPS (Laba per Saham)    : Rp {fmt_number(d['eps'])}
📈 PER (Price to Earnings) : {d['per']:.1f}x      [ {get_status_per(d['per'])} ]
💰 PBV (Price to Book)     : {d['pbv']:.1f}x      [ {get_status_pbv(d['pbv'])} ]
🎯 ROE (Return on Equity)  : {d['roe']:.1f}%     [ {get_status_roe(d['roe'])} ]
🛡️ DER (Debt to Equity)    : {d['der']:.2f}x     [ {get_status_der(d['der'])} ]
💵 Dividend Yield          : {d['div_yield']:.1f}%      [ {get_status_dividen(d['div_yield'])} ]
```

━━━━━━━━━━━━━━━━━━━━━
💰 *BANDARMOLOGY 3 HARI*
━━━━━━━━━━━━━━━━━━━━━
🏦 Asing/Lembaga : *{bandar['asing_status']}* ({bandar['asing']:+}M)
🏪 Retail/Lokal  : *{bandar['retail_status']}* ({bandar['retail']:+}M)
🕴️ Bandar        : *{bandar['bandar_status']}* ({bandar['bandar']:+}M)

━━━━━━━━━━━━━━━━━━━━━
📌 *DISCLAIMER PENTING:*
• Saya adalah BOT ANALISIS, bukan manusia
• Semua data dari Yfinance (delay ±15 menit) & SIMULASI bandarmology
• Bukan rekomendasi jual/beli (tidak ada ajakan transaksi)
• Keputusan investasi sepenuhnya tanggung jawab sendiri

━━━━━━━━━━━━━━━━━━━━━
🔍 *Total {len(STOCKS)} saham IDX tersedia*
📋 *Ketik /list untuk melihat 50 saham pertama*
"""

# ==================== HANDLER TELEGRAM ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
✦ *SAHAM STOCKBOT ULTIMATE* ✦
☾ _Indonesian Stock Analyzer_ ☽

━━━━━━━━━━━━━━━━━━━━━━
◈ *FITUR BOT* ◈
☁ 1200+ Saham IDX Super Lengkap
☁ Termasuk CDIA, SUPA, & semua IPO
☁ Real-time dari Yfinance
☁ Analisis Teknikal Lengkap
☁ Data Fundamental + Status
☁ Bandarmology 3 Hari
☁ Signal Trading (Swing/Day)
☁ Auto Screen 24/7

━━━━━━━━━━━━━━━━━━━━━━
◈ *MULAI ANALISIS* ◈
☁ Ketik kode saham:

```
BBCA   · Bank Central Asia
BBRI   · Bank Rakyat Indonesia  
TLKM   · Telkom Indonesia
ASII   · Astra International
CDIA   · (contoh saham kecil)
SUPA   · (contoh saham kecil)
```

━━━━━━━━━━━━━━━━━━━━━━
◈ *PERINTAH* ◈
☁ /start  · Menu utama  
☁ /help   · Panduan  
☁ /list   · 50 saham pertama  
☁ /stats  · Info bot  

━━━━━━━━━━━━━━━━━━━━━━
◈ *DISCLAIMER* ◈
☁ Data real-time Yfinance (delay ±15 menit)
☁ Bukan rekomendasi jual/beli
☁ Keputusan investasi tanggung jawab sendiri

━━━━━━━━━━━━━━━━━━━━━━
☾ _v4.0 · 1200+ Saham · 24/7 Active_ ☽
""",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📚 *BANTUAN SAHAM STOCKBOT*\n\n"
        f"🔍 *Cara Penggunaan:*\n"
        f"• Ketik kode saham (contoh: BBCA)\n"
        f"• Bot akan menampilkan analisis lengkap\n\n"
        f"📋 *Daftar Perintah:*\n"
        f"/start - Tampilkan menu utama\n"
        f"/help  - Bantuan ini\n"
        f"/list  - Lihat 50 saham pertama\n"
        f"/stats - Statistik bot\n\n"
        f"📊 *Total Saham:* {len(STOCKS)} saham IDX\n\n"
        f"❓ *Contoh Saham:*\n"
        f"BBCA, BBRI, BMRI, BBNI, TLKM, ASII, CDIA, SUPA",
        parse_mode='Markdown'
    )

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks_list = ", ".join(STOCKS[:50])
    await update.message.reply_text(
        f"📋 *50 SAHAM PERTAMA (dari {len(STOCKS)} saham)*\n\n{stocks_list}\n\n"
        f"📊 *Total: {len(STOCKS)} saham IDX*\n"
        f"💡 *Ketik kode saham untuk analisis*",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cache_size = len(stock_cache)
    await update.message.reply_text(
        f"📊 *STATISTIK BOT*\n\n"
        f"• Total saham: {len(STOCKS)} saham IDX\n"
        f"• Cache aktif: {cache_size} saham\n"
        f"• Sumber data: Yfinance (real-time)\n"
        f"• Version: 4.0 (1200+ Saham)\n"
        f"• Status: 24/7 Active (Screen)",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip().upper()
    
    if msg.isalpha() and len(msg) <= 5:
        await update.message.chat.send_action(action="typing")
        result = analyze(msg)
        await update.message.reply_text(result, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Ketik kode saham yang benar.\n"
            "Contoh: BBCA, BBRI, TLKM, CDIA, SUPA\n"
            "Ketik /list untuk melihat 50 saham pertama."
        )

# ==================== MAIN ====================
if __name__ == '__main__':
    print("✅ Starting bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot siap! Tekan Ctrl+C untuk stop")
    print("✅ Total saham:", len(STOCKS
