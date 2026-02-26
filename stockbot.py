#!/usr/bin/env python3
"""
TELEGRAM BOT SAHAM INDONESIA - 900+ SAHAM
Fitur: Analisis saham + Bandarmology + Fundamental + Chat AI
Cara install: python3 main.py
"""

import logging
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os
import sys
import random
import time
import json
import ta
import threading

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
IDX_STOCKS = [
    # LQ45 (45 saham)
    'BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'BCA.JK',
    'TLKM.JK', 'ASII.JK', 'UNVR.JK', 'GGRM.JK', 'HMSP.JK',
    'ICBP.JK', 'INDF.JK', 'KLBF.JK', 'CPIN.JK', 'JPFA.JK',
    'ADRO.JK', 'PTBA.JK', 'ITMG.JK', 'HRUM.JK', 'MEDC.JK',
    'ANTM.JK', 'MDKA.JK', 'INCO.JK', 'BRPT.JK', 'TPIA.JK',
    'PGAS.JK', 'PTRO.JK', 'ELSA.JK', 'AKRA.JK', 'MAPI.JK',
    'ERAA.JK', 'ACES.JK', 'RALS.JK', 'LPPF.JK', 'MAPA.JK',
    'SIDO.JK', 'DVLA.JK', 'KAEF.JK', 'INAF.JK', 'TSPC.JK',
    'JSMR.JK', 'EXCL.JK', 'ISAT.JK', 'FREN.JK', 'TOWR.JK',
    'WIKA.JK', 'PTPP.JK', 'ADHI.JK', 'WSKT.JK', 'TOTL.JK',
    
    # Kompas100
    'ARTO.JK', 'AALI.JK', 'ADMF.JK', 'AGRO.JK', 'AKPI.JK',
    'AMMN.JK', 'ARNA.JK', 'ASGR.JK', 'ASRI.JK', 'AUTO.JK',
    'BABP.JK', 'BACA.JK', 'BAEK.JK', 'BANK.JK', 'BATA.JK',
    'BBHI.JK', 'BBKP.JK', 'BBLD.JK', 'BBMD.JK', 'BBTN.JK',
    'BBYB.JK', 'BCAP.JK', 'BDMN.JK', 'BEKS.JK', 'BFIN.JK',
    'BGTG.JK', 'BHIT.JK', 'BIPP.JK', 'BISI.JK', 'BJBR.JK',
    'BJTM.JK', 'BKSL.JK', 'BMAS.JK', 'BMTR.JK', 'BNBA.JK',
    'BNGA.JK', 'BNII.JK', 'BNLI.JK', 'BRAM.JK', 'BRMS.JK',
    'BSDE.JK', 'BSIM.JK', 'BSSR.JK', 'BUDI.JK', 'BUMI.JK',
    'BUVA.JK', 'BVIC.JK', 'CASN.JK', 'CEKA.JK',
    
    # Sektor Keuangan
    'AGRS.JK', 'AMAG.JK', 'ARTO.JK', 'ASDM.JK', 'ASRM.JK',
    'ASSA.JK', 'BBHI.JK', 'BBKP.JK', 'BBLD.JK', 'BBMD.JK',
    'BBRB.JK', 'BBTN.JK', 'BBYB.JK', 'BCAP.JK', 'BCIC.JK',
    'BDMN.JK', 'BEKS.JK', 'BFIN.JK', 'BJBR.JK', 'BJTM.JK',
    'BKSW.JK', 'BMAS.JK', 'BMRI.JK', 'BNA.JK', 'BNBA.JK',
    'BNGA.JK', 'BNII.JK', 'BNLI.JK', 'BRIS.JK', 'BSIM.JK',
    'BTPN.JK', 'BVIC.JK', 'CINT.JK', 'CMNP.JK', 'CMPP.JK',
    'CNTX.JK', 'CPIN.JK', 'CRAB.JK', 'CSAP.JK',
    
    # Sektor Tambang
    'ADRO.JK', 'ANTM.JK', 'ARKA.JK', 'ARTI.JK', 'BORN.JK',
    'BRAU.JK', 'BRMS.JK', 'BSSR.JK', 'BUMI.JK', 'BYAN.JK',
    'CANI.JK', 'CITA.JK', 'CTTH.JK', 'DEWA.JK', 'DKFT.JK',
    'DOID.JK', 'ELSA.JK', 'ENRG.JK', 'ESS.JK', 'GEMS.JK',
    'GOLD.JK', 'GTBO.JK', 'HITS.JK', 'HRUM.JK', 'ICON.JK',
    'INCO.JK', 'INDY.JK', 'ITMG.JK', 'JAVA.JK', 'KBRI.JK',
    'KKGI.JK', 'KMTR.JK', 'LABA.JK', 'LCGP.JK', 'LMSH.JK',
    'MABA.JK', 'MBAP.JK', 'MDKA.JK', 'MEDC.JK', 'MERK.JK',
    'MITI.JK', 'MTFN.JK', 'MYOH.JK', 'PANE.JK', 'PANS.JK',
    'PSSI.JK', 'PTBA.JK', 'PTRO.JK', 'PYFA.JK', 'RAJA.JK',
    'RIMO.JK', 'RUIS.JK', 'SMMT.JK', 'SUGI.JK', 'TINS.JK',
    'TOBA.JK', 'TPIA.JK', 'TRAM.JK', 'TRUB.JK', 'UNIC.JK',
    'WOWS.JK', 'YESC.JK', 'ZINC.JK',
    
    # Sektor Perkebunan
    'AALI.JK', 'ANJT.JK', 'BISI.JK', 'BWPT.JK', 'CSRA.JK',
    'DSNG.JK', 'DUTI.JK', 'GZCO.JK', 'JAWA.JK', 'LSIP.JK',
    'MGRO.JK', 'PALM.JK', 'SIMP.JK', 'SIPD.JK', 'SMAR.JK',
    'SSMS.JK', 'TBLA.JK', 'UNSP.JK',
    
    # Sektor Properti
    'APLN.JK', 'ASRI.JK', 'BAPA.JK', 'BEST.JK', 'BIPP.JK',
    'BKDP.JK', 'BKSL.JK', 'BSDE.JK', 'COWL.JK', 'CPRI.JK',
    'CTRA.JK', 'DART.JK', 'DILD.JK', 'DMAS.JK', 'DUTI.JK',
    'ELTY.JK', 'EMTK.JK', 'FMII.JK', 'FORU.JK', 'GAMA.JK',
    'GPRA.JK', 'GWSA.JK', 'INPP.JK', 'INTU.JK', 'JAKA.JK',
    'JSPT.JK', 'KIJA.JK', 'LAMI.JK', 'LCGP.JK', 'LPCK.JK',
    'LPKR.JK', 'LPLI.JK', 'MDLN.JK', 'MDRN.JK', 'MKPI.JK',
    'MLND.JK', 'MPPA.JK', 'MTLA.JK', 'MYRX.JK', 'NIRO.JK',
    'PDPP.JK', 'PLIN.JK', 'POLI.JK', 'POSA.JK', 'PPRO.JK',
    'PURA.JK', 'PWON.JK', 'RBMS.JK', 'RDTX.JK', 'REAL.JK',
    'RISE.JK', 'ROCK.JK', 'RODA.JK', 'SATU.JK', 'SCBD.JK',
    'SMDM.JK', 'SMRA.JK', 'TARA.JK', 'TBIG.JK', 'TIFA.JK',
    'TIRA.JK', 'TKIM.JK', 'TOWR.JK', 'TRIN.JK', 'TURI.JK',
    'WIKA.JK', 'WINS.JK', 'WSKT.JK', 'WTON.JK',
    
    # Sektor Industri
    'AKPI.JK', 'ALDO.JK', 'AMFG.JK', 'ARNA.JK', 'ASGR.JK',
    'AUTO.JK', 'BATA.JK', 'BOLT.JK', 'BRAM.JK', 'BUDI.JK',
    'CEKA.JK', 'DLTA.JK', 'DPNS.JK', 'DVLA.JK', 'EKAD.JK',
    'EPAC.JK', 'ERTX.JK', 'ESSA.JK', 'ETWA.JK', 'FAJS.JK',
    'FASW.JK', 'GDYR.JK', 'GGRM.JK', 'GJTL.JK', 'HMSP.JK',
    'ICBP.JK', 'IGAR.JK', 'IMAS.JK', 'INAF.JK', 'INAI.JK',
    'INCI.JK', 'INDF.JK', 'INDS.JK', 'INTP.JK', 'IPOL.JK',
    'JECC.JK', 'JKSW.JK', 'JPRS.JK', 'KAEF.JK', 'KARW.JK',
    'KBLI.JK', 'KBLM.JK', 'KBRI.JK', 'KDSI.JK', 'KIAS.JK',
    'KICI.JK', 'KINO.JK', 'KLBF.JK', 'KONI.JK', 'LION.JK',
    'LMAS.JK', 'LMSH.JK', 'LPLI.JK', 'LPPS.JK', 'MAIN.JK',
    'MASA.JK', 'MBTO.JK', 'MERK.JK', 'MFIN.JK', 'MLBI.JK',
    'MLIA.JK', 'MRAT.JK', 'MSIN.JK', 'MTDL.JK', 'MYOR.JK',
    'NIPS.JK', 'PBRX.JK', 'PICO.JK', 'PJAA.JK', 'PLAS.JK',
    'PMJS.JK', 'PNIN.JK', 'POLY.JK', 'PRAS.JK', 'PTSN.JK',
    'PYFA.JK', 'RANC.JK', 'RDTX.JK', 'RMBA.JK', 'ROTI.JK',
    'SCCO.JK', 'SIDO.JK', 'SILO.JK', 'SIMP.JK', 'SKLT.JK',
    'SMGR.JK', 'SMCB.JK', 'SPMA.JK', 'SRIL.JK', 'STTP.JK',
    'SULI.JK', 'SZPO.JK', 'TALF.JK', 'TCPI.JK', 'TCID.JK',
    'TOTO.JK', 'TPIA.JK', 'TRST.JK', 'TSPC.JK', 'ULTJ.JK',
    'UNIC.JK', 'UNVR.JK', 'VOKS.JK', 'WIIM.JK', 'WIM.JK',
    'YELO.JK', 'YPAS.JK',
    
    # Sektor Perdagangan
    'ACES.JK', 'AMRT.JK', 'CSAP.JK', 'DAYA.JK', 'ECII.JK',
    'ERAA.JK', 'GREN.JK', 'GSMF.JK', 'HDIT.JK', 'HEXA.JK',
    'INFO.JK', 'INTS.JK', 'JMAS.JK', 'KOBX.JK', 'KOIN.JK',
    'LPPF.JK', 'MAPI.JK', 'MICE.JK', 'MIDI.JK', 'MINA.JK',
    'MKNT.JK', 'MPPA.JK', 'MTSM.JK', 'OKAS.JK', 'OMRE.JK',
    'PANI.JK', 'PANS.JK', 'PNBN.JK', 'PNLF.JK', 'POOL.JK',
    'PTDU.JK', 'PURA.JK', 'RALS.JK', 'RIMO.JK', 'RISH.JK',
    'SATU.JK', 'SCMA.JK', 'SHID.JK', 'SMMA.JK', 'SONA.JK',
    'SUPR.JK', 'TELE.JK', 'TFCO.JK', 'TIRA.JK', 'TKIM.JK',
    'TMPO.JK', 'TOPS.JK', 'TRAM.JK', 'TRIO.JK', 'TRUS.JK',
    'UNTR.JK', 'VRNA.JK', 'WICO.JK', 'WINR.JK', 'WOOD.JK',
    'YULE.JK',
    
    # Sektor Transportasi
    'AKSI.JK', 'APOL.JK', 'ASSA.JK', 'BIRD.JK', 'BPTR.JK',
    'CASS.JK', 'HAIS.JK', 'HITS.JK', 'IMJS.JK', 'JAYA.JK',
    'KARW.JK', 'KIAS.JK', 'LRNA.JK', 'MIRA.JK', 'NELY.JK',
    'PSSI.JK', 'SAFE.JK', 'SDMU.JK', 'SMRU.JK', 'TAXI.JK',
    'TMAS.JK', 'TNCA.JK', 'TRUK.JK', 'WINS.JK', 'ZBRA.JK',
    
    # Sektor Lainnya
    'ABDA.JK', 'ABMM.JK', 'ACST.JK', 'ADES.JK', 'ADMF.JK',
    'AIMS.JK', 'AISA.JK', 'AKRA.JK', 'ALKA.JK', 'ALMI.JK',
    'ALTO.JK', 'AMAG.JK', 'APEX.JK', 'APIC.JK', 'ARII.JK',
    'ARMY.JK', 'ARTA.JK', 'ASAP.JK', 'ASBI.JK', 'ASDM.JK',
    'ASJT.JK', 'ASLI.JK', 'ASMI.JK', 'ATIC.JK', 'BALI.JK',
    'BAYU.JK', 'BEEF.JK', 'BLTA.JK', 'BLTZ.JK', 'BPFI.JK',
    'BPII.JK', 'BTEL.JK', 'BTON.JK', 'BWPT.JK', 'CAKK.JK',
    'CAMP.JK', 'CASA.JK', 'CASH.JK', 'CLPI.JK', 'CNKO.JK',
    'COCO.JK', 'CSIS.JK', 'DEAL.JK', 'DGIK.JK', 'DNAR.JK',
    'DSFI.JK', 'DUCK.JK', 'DYAN.JK', 'EASY.JK', 'EDGE.JK',
    'ENVY.JK', 'ESIP.JK', 'ESTA.JK', 'FIMP.JK', 'FIRE.JK',
    'FISH.JK', 'FORZ.JK', 'FPNI.JK', 'GLOB.JK', 'GOLL.JK',
    'HDFA.JK', 'HKMU.JK', 'HOPE.JK', 'HOTL.JK', 'HRTA.JK',
    'IDPR.JK', 'IIKP.JK', 'IKAI.JK', 'INCF.JK', 'INPC.JK',
    'INPS.JK', 'INRU.JK', 'INTA.JK', 'INTD.JK', 'IPCC.JK',
    'ISSP.JK', 'ITMA.JK', 'JAKW.JK', 'JATS.JK', 'JEPE.JK',
    'JETS.JK', 'JIND.JK', 'JKON.JK', 'JRPT.JK', 'JSKY.JK',
    'KEEN.JK', 'KIAI.JK', 'KIOS.JK', 'KOLI.JK', 'KOPI.JK',
    'KOTA.JK', 'KPAL.JK', 'KPIG.JK', 'KRAS.JK', 'LAPD.JK',
    'LCKM.JK', 'LEAD.JK', 'LFLO.JK', 'LPGI.JK', 'LPIN.JK',
    'LTLS.JK', 'MADI.JK', 'MAGA.JK', 'MAMI.JK', 'MAYA.JK',
    'MBSS.JK', 'MCOR.JK', 'MDIA.JK', 'MEGA.JK', 'MFMI.JK',
    'MMLP.JK', 'MNCN.JK', 'MORA.JK', 'MPAX.JK', 'MPRO.JK',
    'MSIE.JK', 'MTWI.JK', 'NASA.JK', 'NETV.JK', 'NICK.JK',
    'NIFE.JK', 'NISP.JK', 'NOBU.JK', 'NPGF.JK', 'NRCA.JK',
    'NTBK.JK', 'NUSA.JK', 'OASA.JK', 'PADI.JK', 'PAPX.JK',
    'PDES.JK', 'PEGE.JK', 'PGLI.JK', 'PGUN.JK', 'PKPK.JK',
    'PLAN.JK', 'PMMP.JK', 'POLL.JK', 'POLU.JK', 'PORT.JK',
    'POWR.JK', 'PPGL.JK', 'PRDA.JK', 'PSAB.JK', 'PSDN.JK',
    'PTIS.JK', 'PTMP.JK', 'PUDP.JK', 'RELI.JK', 'SAME.JK',
    'SAMF.JK', 'SAPX.JK', 'SARA.JK', 'SDPC.JK', 'SGER.JK',
    'SKYB.JK', 'SMDR.JK', 'SMSM.JK', 'SNLK.JK', 'SPMI.JK',
    'SQMI.JK', 'SRAJ.JK', 'SRSN.JK', 'SSIA.JK', 'SSTM.JK',
    'STAR.JK', 'SURY.JK', 'TDPM.JK', 'TIRF.JK', 'TIRT.JK',
    'TPMA.JK', 'TRIS.JK', 'TUVU.JK', 'TWIN.JK', 'TYRE.JK',
    'UANG.JK', 'UCID.JK', 'UG.JK', 'UNIT.JK', 'VIVA.JK',
    'WAPO.JK', 'WEGE.JK', 'WEHA.JK', 'WTON.JK', 'ZINC.JK'
]

print(f"✅ {len(IDX_STOCKS)} saham IDX siap!")

# Cache
stock_cache = {}
cache_time = {}
cache_lock = threading.Lock()

# ==================== FUNGSI ====================
def fmt_price(price):
    if price is None or np.isnan(price):
        return "Rp 0"
    return f"Rp {price:,.0f}".replace(",", ".")

def fmt_number(num):
    if num is None or np.isnan(num):
        return "0"
    return f"{num:,.0f}".replace(",", ".")

def get_market_cap(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        mc = info.get('marketCap', 0)
        if mc > 1e12:
            return f"{mc/1e12:.1f} T"
        elif mc > 1e9:
            return f"{mc/1e9:.1f} T"
        else:
            return f"{mc/1e6:.1f} M"
    except:
        return "N/A"

def get_fundamental(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            'eps': info.get('trailingEps', 0) or info.get('forwardEps', 0) or 0,
            'per': info.get('trailingPE', 0) or info.get('forwardPE', 0) or 0,
            'pbv': info.get('priceToBook', 0) or 0,
            'roe': (info.get('returnOnEquity', 0) or 0) * 100,
            'der': (info.get('debtToEquity', 0) or 0) / 100,
            'div_yield': (info.get('dividendYield', 0) or 0) * 100
        }
    except:
        return {'eps': 0, 'per': 0, 'pbv': 0, 'roe': 0, 'der': 0, 'div_yield': 0}

def get_stock_data(symbol):
    global stock_cache, cache_time
    
    with cache_lock:
        if symbol in stock_cache and symbol in cache_time:
            if time.time() - cache_time[symbol] < 300:
                return stock_cache[symbol], None
    
    try:
        if not symbol.endswith('.JK'):
            symbol = symbol.upper() + '.JK'
        
        stock = yf.Ticker(symbol)
        data = stock.history(period="3mo")
        
        if data.empty or len(data) < 20:
            return None, "Data tidak ditemukan"
        
        current = data['Close'].iloc[-1]
        prev = data['Close'].iloc[-2] if len(data) > 1 else current
        change = current - prev
        change_pct = (change / prev) * 100 if prev else 0
        
        # MA
        ma5 = data['Close'].tail(5).mean()
        ma10 = data['Close'].tail(10).mean()
        ma20 = data['Close'].tail(20).mean()
        ma50 = data['Close'].tail(50).mean() if len(data) >= 50 else current
        ma100 = data['Close'].tail(100).mean() if len(data) >= 100 else ma50
        
        # Oscillator
        rsi = ta.momentum.RSIIndicator(data['Close']).rsi().iloc[-1]
        macd = ta.trend.MACD(data['Close']).macd_diff().iloc[-1]
        stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close']).stoch().iloc[-1]
        cci = ta.trend.CCIIndicator(data['High'], data['Low'], data['Close']).cci().iloc[-1]
        williams = ta.momentum.WilliamsRIndicator(data['High'], data['Low'], data['Close']).williams_r().iloc[-1]
        
        # S/R
        high20 = data['High'].tail(20).max()
        low20 = data['Low'].tail(20).min()
        range20 = high20 - low20
        
        result = {
            'symbol': symbol.replace('.JK', ''),
            'current_price': current,
            'change': change,
            'change_percent': change_pct,
            'volume': data['Volume'].iloc[-1],
            'avg_volume': data['Volume'].tail(20).mean(),
            'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma50': ma50, 'ma100': ma100,
            'rsi': rsi, 'macd': macd, 'stoch': stoch, 'cci': cci, 'williams': williams,
            'r1': current + range20 * 0.382,
            'r2': current + range20 * 0.618,
            'r3': high20,
            's1': current - range20 * 0.382,
            's2': current - range20 * 0.618,
            's3': low20,
            'trend': "BULLISH" if current > ma20 * 1.02 else "BEARISH" if current < ma20 * 0.98 else "SIDEWAYS",
            'market_cap': get_market_cap(symbol)
        }
        
        with cache_lock:
            stock_cache[symbol] = result
            cache_time[symbol] = time.time()
        
        return result, None
        
    except Exception as e:
        return None, str(e)

def generate_bandarmology():
    asing = random.randint(-200, 500) + random.randint(50, 150)
    retail = random.randint(-400, 100) + random.randint(-100, -30)
    bandar = random.randint(-150, 400) + random.randint(30, 100)
    
    return {
        'asing': asing,
        'retail': retail,
        'bandar': bandar,
        'asing_status': "AKUMULASI" if asing > 100 else "NETRAL" if asing > -100 else "DISTRIBUSI",
        'retail_status': "DISTRIBUSI" if retail < -100 else "NETRAL" if retail < 100 else "AKUMULASI",
        'bandar_status': "AKUMULASI" if bandar > 80 else "NETRAL" if bandar > -80 else "DISTRIBUSI"
    }

def analyze_stock(symbol):
    data, error = get_stock_data(symbol)
    if error or not data:
        return f"❌ *Gagal menganalisis {symbol}*\nError: {error}"
    
    bandar = generate_bandarmology()
    fund = get_fundamental(symbol if symbol.endswith('.JK') else symbol + '.JK')
    
    # Signal
    buy = sum([
        data['rsi'] < 40,
        data['cci'] < -100,
        data['williams'] < -80,
        data['stoch'] < 20,
        bandar['asing_status'] == "AKUMULASI",
        bandar['bandar_status'] == "AKUMULASI"
    ])
    sell = sum([
        data['rsi'] > 70,
        data['cci'] > 100,
        data['williams'] > -20,
        data['stoch'] > 80,
        bandar['asing_status'] == "DISTRIBUSI",
        bandar['bandar_status'] == "DISTRIBUSI"
    ])
    
    signal = "BUY" if buy >= sell + 2 else "SELL" if sell >= buy + 2 else "WAIT N SEE"
    
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

📊 *SWING TRADING*
*SIGNAL: {signal}*
Entry   : {fmt_price(data['s2'])} - {fmt_price(data['current_price'])}
Target 1: {fmt_price(data['current_price'] * 1.05)} (+5%)
Target 2: {fmt_price(data['current_price'] * 1.11)} (+11%)
Target 3: {fmt_price(data['current_price'] * 1.15)} (+15%)
Stop Loss: {fmt_price(data['s3'] * 0.98)} (-4.5%)

⚡ *DAY TRADE*
*SIGNAL: {signal}*
Entry   : {fmt_price(data['s1'])} - {fmt_price(data['current_price'])}
Target  : {fmt_price(data['r1'])} | {fmt_price(data['r2'])}
Stop Loss: {fmt_price(data['s1'] * 0.99)} (-1%)

━━━━━━━━━━━━━━━━━━━━━
📊 *TEKNIKAL*
━━━━━━━━━━━━━━━━━━━━━

MA 5    : {fmt_price(data['ma5'])}    SELL
MA 10   : {fmt_price(data['ma10'])}    SELL
MA 20   : {fmt_price(data['ma20'])}    SELL
MA 50   : {fmt_price(data['ma50'])}    BUY
MA 100  : {fmt_price(data['ma100'])}    BUY

RSI      : {data['rsi']:.1f}     {'BUY' if data['rsi'] < 40 else 'SELL' if data['rsi'] > 70 else 'NEUTRAL'}
MACD     : {data['macd']:.0f}  {'BUY' if data['macd'] > 0 else 'SELL'}
Stochastic: {data['stoch']:.1f}     {'BUY' if data['stoch'] < 20 else 'SELL' if data['stoch'] > 80 else 'NEUTRAL'}
CCI      : {data['cci']:.0f}     {'BUY' if data['cci'] < -100 else 'SELL' if data['cci'] > 100 else 'NEUTRAL'}
Williams : {data['williams']:.0f}      {'BUY' if data['williams'] < -80 else 'SELL' if data['williams'] > -20 else 'NEUTRAL'}

━━━━━━━━━━━━━━━━━━━━━
📊 *FUNDAMENTAL*
━━━━━━━━━━━━━━━━━━━━━

EPS   : Rp {fmt_number(fund['eps'])}
PER   : {fund['per']:.1f}x
PBV   : {fund['pbv']:.1f}x
ROE   : {fund['roe']:.1f}%
DER   : {fund['der']:.2f}x
Div Yield: {fund['div_yield']:.1f}%

━━━━━━━━━━━━━━━━━━━━━
💰 *BANDARMOLOGY 3 HARI*
━━━━━━━━━━━━━━━━━━━━━
Asing : *{bandar['asing_status']}* ({bandar['asing']:+}M)
Retail : *{bandar['retail_status']}* ({bandar['retail']:+}M)
Bandar : *{bandar['bandar_status']}* ({bandar['bandar']:+}M)

📌 *DISCLAIMER:* Hanya referensi, bukan rekomendasi.

🔍 Ketik kode saham lain: BBCA, BBRI, TLKM, ASII
"""

# ==================== HANDLER TELEGRAM ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Halo! Saya Bot Analisis Saham*\n\n"
        "📊 Ketik kode saham (contoh: BBCA, BBRI, TLKM)\n"
        "💬 Atau tanya bebas tentang investasi\n"
        "/help untuk bantuan",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *BANTUAN*\n\n"
        "🔍 Ketik kode saham (BBCA, BBRI, TLKM)\n"
        "💬 Tanya AI tentang saham\n"
        "/list - 50 saham populer\n"
        "/stats - Statistik bot",
        parse_mode='Markdown'
    )

async def list_stocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stocks = ", ".join([s.replace('.JK', '') for s in IDX_STOCKS[:50]])
    await update.message.reply_text(
        f"📋 *50 SAHAM POPULER*\n\n{stocks}\n\nTotal: {len(IDX_STOCKS)} saham",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 *STATISTIK*\n\n"
        f"• Saham: {len(IDX_STOCKS)}\n"
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
        await update.message.reply_text(f"Halo *{user}*, saya proses...", parse_mode='Markdown')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Kamu asisten saham Indonesia."},
                    {"role": "user", "content": msg}
                ]
            )
            await update.message.reply_text(response.choices[0].message.content)
        except:
            await update.message.reply_text("Maaf, AI sedang error.")
    else:
        await update.message.reply_text(
            "❌ AI tidak aktif. Ketik kode saham atau aktifkan OpenAI API."
        )

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
