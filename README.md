
# 🤖 BOT SAHAM TELEGRAM INDONESIA

Bot Telegram untuk informasi saham Indonesia, analisis teknikal, screening, dan konsultasi AI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Telegram](https://img.shields.io/badge/telegram-bot-blue)
![License](https://img.shields.io/badge/license-MIT-orange)
![Ubuntu](https://img.shields.io/badge/ubuntu-18.04+-orange)
![Debian](https://img.shields.io/badge/debian-10+-red)

---

## 📋 DAFTAR ISI
• [🔗 Link Install](#🔗-link-install)
• [✨ Fitur Lengkap](#✨-fitur-lengkap)
• [📸 Screenshot](#📸-screenshot)
• [🚀 Cara Install](#🚀-cara-install)
• [🔄 Cara Upgrade](#🔄-cara-upgrade)
• [⏰ Menjaga Bot Tetap Aktif 24/7](#⏰-menjaga-bot-tetap-aktif-247)
• [📁 Struktur File](#📁-struktur-file)
• [📄 Daftar File Bot](#📄-daftar-file-bot)
• [⚙️ Konfigurasi](#⚙️-konfigurasi)
• [📊 Command List](#📊-command-list)
• [🚨 Troubleshooting](#🚨-troubleshooting)
• [📝 Lisensi](#📝-lisensi)

---

## 🔗 LINK INSTALL

### ⚡ INSTALL 1 DETIK
```bash
wget -O install.sh https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh && chmod +x install.sh && ./install.sh
```

### 📥 DOWNLOAD MANUAL
```bash
# Download script installer
wget https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh

# Beri permission
chmod +x saham.sh

# Jalankan
./saham.sh
```

### 📂 REPOSITORY GITHUB
```
https://github.com/script-VIP/bott
```

### 📄 FILE RAW LINKS
| File | Link |
|------|------|
| **Main Installer** | [`saham.sh`](https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh) |
| **Main Bot** | [`bot.py`](https://raw.githubusercontent.com/script-VIP/bott/main/bot.py) |
| **Konfigurasi** | [`config.py`](https://raw.githubusercontent.com/script-VIP/bott/main/config.py) |
| **Database** | [`database.py`](https://raw.githubusercontent.com/script-VIP/bott/main/database.py) |
| **Handler Saham** | [`saham_handler.py`](https://raw.githubusercontent.com/script-VIP/bott/main/saham_handler.py) |
| **AI Handler** | [`ai_handler.py`](https://raw.githubusercontent.com/script-VIP/bott/main/ai_handler.py) |
| **Keep Alive** | [`keep_alive.py`](https://raw.githubusercontent.com/script-VIP/bott/main/keep_alive.py) |
| **Dependencies** | [`requirements.txt`](https://raw.githubusercontent.com/script-VIP/bott/main/requirements.txt) |
| **Dokumentasi** | [`README.md`](https://raw.githubusercontent.com/script-VIP/bott/main/README.md) |

---

## ✨ FITUR LENGKAP

### 🤖 **TANYA AI SEPUTAR SAHAM**
Fitur tanya jawab dengan AI untuk membantu Anda memahami dunia saham.

**🔍 Topik yang bisa ditanyakan:**
• **Indikator Teknikal**: RSI, MACD, Moving Average, Stochastic, CCI, Williams %R
• **Analisis Fundamental**: P/E Ratio, PBV, ROE, DER, Valuasi Saham
• **Pola Chart**: Double Bottom, Head & Shoulders, Candlestick Patterns
• **Strategi Trading**: Day Trade, Swing Trade, Long Term, Scalping
• **Edukasi Saham**: Istilah-istilah saham, Cara baca laporan keuangan
• **Analisis Saham Spesifik**: Tanya tentang BBCA, TLKM, BBRI, dll

**💡 Contoh Pertanyaan:**
• "Apa artinya RSI 34.7 pada BBCA?"
• "Jelaskan pola double bottom"
• "Bagaimana prospek saham perbankan 2026?"
• "Apa indikator terbaik untuk day trade?"
• "Kapan waktu yang tepat buy the dip?"

### 📈 **ANALISIS SAHAM INDIVIDUAL**
Analisis lengkap untuk setiap saham dengan data real-time.

**📊 DATA HARGA:**
• Harga terkini
• Perubahan harga (Rp & Persentase)
• Update timestamp

**🎯 SIGNAL DAY TRADE (INTRADAY):**
• Signal: BUY / SELL / HOLD
• Entry area (support)
• Target 1, 2, 3 (profit taking)
• Stop Loss
• Alasan teknikal & volume

**📊 SIGNAL SWING TRADING (3 HARI - 1 BULAN):**
• Signal: BUY / SELL / HOLD
• Entry area
• Target 1, 2, 3
• Stop Loss
• Alasan teknikal & bandarmology

**📉 TEKNIKAL LENGKAP:**
• **Moving Average**: MA5, MA10, MA20, MA50, MA100 + sinyal (DI ATAS/DI BAWAH)
• **Oscillator**: RSI (status oversold/overbought), MACD (bullish/bearish)
• **Kesimpulan indikator** dari multiple timeframe

**💰 BANDARMOLOGY:**
• Net buy/sell: Asing, Asing NG, Retail, Mutual Fund
• Movement Index (0-100)
• Kesimpulan: Akumulasi / Distribusi

**🛡️ SUPPORT & RESISTANCE:**
• R3, R2, R1 (Resistance 3 level)
• S1, S2, S3 (Support 3 level)
• Level psikologis dan teknikal

**⚠️ RISK WARNING:**
• Level kritis
• Rekomendasi stop loss
• Peringatan risiko

### 📊 **SCREENING SAHAM**
Menampilkan saham-saham berdasarkan kriteria tertentu.

**🔥 TOP MOMENTUM:**
• Saham dengan kenaikan tertinggi
• Gap up + volume spike
• Breakout resistance

**💡 REBOUND POTENTIAL:**
• Saham oversold (RSI < 35)
• Dekat support kuat
• Potensi reversal

**💎 BANDAR & ASING AKUMULASI:**
• **Periode**: 1 Hari / 3 Hari / 5 Hari
• Data net buy asing & bandar
• Rekomendasi entry area

**🚀 BREAKOUT & RESISTEN:**
• Saham yang baru break resistance
• Konfirmasi volume
• Target selanjutnya

**🛡️ AREA SUPPORT:**
• Saham yang menyentuh support kuat
• MA50, MA100, atau level psikologis
• Potensi pantulan

**🔄 POTENSI TUTUP GAP:**
• Gap atas (potensi naik)
• Gap bawah (potensi turun)
• Jarak ke gap

**🥈 DOUBLE BOTTOM:**
• Pola reversal bullish
• Bottom 1 & Bottom 2
• Neckline dan target

**⬆️ ON PULLBACK:**
• Saham yang sedang pullback ke support
• Entry opportunity
• Support MA20/MA50

**📊 SWING TRADING:**
• Kandidat swing trading (3H-1B)
• Entry, target, stop loss
• Alasan lengkap

**⚡ DAY TRADE:**
• Kandidat day trade intraday
• Range harga
• Target 1-3% dengan stop loss ketat

**📈 LONG TERM:**
• Kandidat investasi 1-3 bulan
• Fundamental kuat
• Target 15-30%

**📉 OPEN LOW:**
• Saham open low tapi mulai rebound
• Potensi reversal intraday

**📈 OPEN HIGH:**
• Saham open high dengan momentum
• Konfirmasi volume

### 🔔 **FITUR TAMBAHAN**

**📈 IHSG & INDEKS:**
• IHSG (Indeks Harga Saham Gabungan)
• LQ45
• IDX30
• Perubahan dan persentase

**💰 TOP GAINER & LOSER:**
• 5 saham dengan kenaikan tertinggi
• 5 saham dengan penurunan tertinggi
• Volume dan harga

**⭐ WATCHLIST:**
• Tambah saham ke watchlist
• Lihat semua pantauan
• Hapus dari watchlist

**🔔 NOTIFIKASI:**
• Notifikasi harga target
• Notifikasi perubahan >5%
• Atur notifikasi per saham

---

## 📸 SCREENSHOT

```
🤖 BOT INFORMASI SAHAM INDONESIA
🕐 Update: 20/02/2026 14:30 WIB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Halo User! Selamat datang di Bot Saham Indonesia!

📌 LAYANAN BOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 Tanya AI seputar saham
🔍 Cari informasi saham terkini
📈 Analisis teknikal & fundamental
💰 Screening saham berdasarkan kriteria
🔔 Notifikasi harga & watchlist
```

```
📈 ANALISIS SAHAM BBCA
🕐 Update: 20/02/2026 14:30 WIB
💰 Harga: Rp 7,175.00
📊 Perubahan: -100.00 (-1.37%)

🎯 SIGNAL DAY TRADE
SIGNAL: BUY (AGRESIF)
Entry   : Rp 7,139 - 7,175
Target 1: Rp 7,246 (+1%)
Target 2: Rp 7,320 (+2%)
Target 3: Rp 7,400 (+3%)
Stop Loss: Rp 7,103 (-1%)

📊 TEKNIKAL
MA5 : Rp 7,285 (DI BAWAH) BEARISH
MA20: Rp 7,290 (DI BAWAH) BEARISH
MA50: Rp 7,150 (DI ATAS)  BULLISH
RSI : 34.7 (OVERSOLD)
MACD: -172.08 (BEARISH)
```

```
📊 SCREENING: SWING TRADING
🕐 Update: 20/02/2026 14:30 WIB

1. BBCA    Rp 7,175
   Entry: 7,031 - 7,175
   T1: 7,550 | T2: 7,950 | T3: 8,250
   SL: 6,850
   Alasan: Oversold + support MA100

2. TLKM    Rp 3,890
   Entry: 3,880 - 3,890
   T1: 4,020 | T2: 4,150 | T3: 4,300
   SL: 3,820
   Alasan: Double bottom + RSI 32
```

---

## 🚀 CARA INSTALL

### **PRASYARAT**
• Ubuntu 18.04+ / Debian 10+ / Termux (Android)
• Python 3.7+
• Token bot dari [@BotFather](https://t.me/BotFather)

### **METODE 1: INSTALL OTOMATIS (REKOMENDASI)**

```bash
# 1. Download dan jalankan installer (1 detik)
wget -O install.sh https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh && chmod +x install.sh && ./install.sh

# Atau step by step:
wget https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh
chmod +x saham.sh
./saham.sh
```

**Menu Installer:**
• **Menu 1**: Install dengan Screen (mudah)
• **Menu 2**: Install dengan Systemd (rekomendasi 24/7)
• **Menu 3**: Install dengan Tmux (alternatif)
• **Menu 4**: Start Bot
• **Menu 5**: Stop Bot
• **Menu 6**: Restart Bot
• **Menu 7**: Cek Status
• **Menu 8**: Lihat Log
• **Menu 9**: Update Bot
• **Menu 10**: Backup Database
• **Menu 11**: Restore Database
• **Menu 12**: Uninstall Bot

### **METODE 2: INSTALL MANUAL**

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3 python3-pip git screen wget curl

# 3. Buat folder
mkdir -p ~/tele-saham-bot
cd ~/tele-saham-bot

# 4. Download semua file
wget https://raw.githubusercontent.com/script-VIP/bott/main/bot.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/config.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/database.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/saham_handler.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/ai_handler.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/keep_alive.py
wget https://raw.githubusercontent.com/script-VIP/bott/main/requirements.txt

# 5. Install Python packages
pip3 install -r requirements.txt

# 6. Buat file .env
nano .env
# Isi dengan: BOT_TOKEN=token_anda_disini

# 7. Jalankan bot
python3 bot.py
```

### **METODE 3: INSTALL DI TERMUX (ANDROID)**

```bash
# 1. Update pkg
pkg update && pkg upgrade

# 2. Install dependencies
pkg install python git wget

# 3. Download script
wget https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh
chmod +x saham.sh
bash saham.sh
```

---

## 🔄 CARA UPGRADE

### **UPGRADE DENGAN SCRIPT**
```bash
# Jalankan script installer
cd ~
wget -O install.sh https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh
chmod +x install.sh
./install.sh
```
Lalu pilih menu **9** (Update Bot)

### **UPGRADE MANUAL**
```bash
# Masuk ke folder bot
cd ~/tele-saham-bot

# Download ulang semua file
wget -O bot.py https://raw.githubusercontent.com/script-VIP/bott/main/bot.py
wget -O config.py https://raw.githubusercontent.com/script-VIP/bott/main/config.py
wget -O database.py https://raw.githubusercontent.com/script-VIP/bott/main/database.py
wget -O saham_handler.py https://raw.githubusercontent.com/script-VIP/bott/main/saham_handler.py
wget -O ai_handler.py https://raw.githubusercontent.com/script-VIP/bott/main/ai_handler.py
wget -O keep_alive.py https://raw.githubusercontent.com/script-VIP/bott/main/keep_alive.py
wget -O requirements.txt https://raw.githubusercontent.com/script-VIP/bott/main/requirements.txt

# Update dependencies
pip3 install --upgrade -r requirements.txt

# Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py
```

---

## ⏰ MENJAGA BOT TETAP AKTIF 24/7

### **METODE 1: SCREEN (PALING MUDAH)**

```bash
# Jalankan di screen
screen -dmS sahabot python3 ~/tele-saham-bot/bot.py

# Lihat session
screen -ls

# Masuk ke session
screen -r sahabot

# Keluar screen: Ctrl+A lalu D

# Matikan bot
screen -X -S sahabot quit
```

### **METODE 2: SYSTEMD (REKOMENDASI PROFESIONAL)**

```bash
# Buat service file
sudo nano /etc/systemd/system/sahabot.service
```

Isi dengan:
```ini
[Unit]
Description=Telegram Saham Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/tele-saham-bot
ExecStart=/usr/bin/python3 /home/$USER/tele-saham-bot/bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/$USER/tele-saham-bot/bot.log
StandardError=append:/home/$USER/tele-saham-bot/bot.log

[Install]
WantedBy=multi-user.target
```

```bash
# Enable dan start
sudo systemctl daemon-reload
sudo systemctl enable sahabot.service
sudo systemctl start sahabot.service

# Cek status
sudo systemctl status sahabot.service

# Lihat log
sudo journalctl -u sahabot.service -f

# Restart
sudo systemctl restart sahabot.service

# Stop
sudo systemctl stop sahabot.service
```

### **METODE 3: TMUX**

```bash
# Install tmux
sudo apt install tmux -y

# Jalankan
tmux new-session -d -s sahabot 'python3 ~/tele-saham-bot/bot.py'

# Masuk tmux
tmux attach -t sahabot

# Keluar: Ctrl+B lalu D

# Matikan
tmux kill-session -t sahabot
```

### **METODE 4: AUTO RESTART DENGAN CRON**

```bash
# Buat cron job untuk cek setiap 5 menit
crontab -e

# Tambahkan baris ini:
*/5 * * * * pgrep -f "python3.*bot.py" || screen -dmS sahabot python3 /home/$USER/tele-saham-bot/bot.py
```

---

## 📁 STRUKTUR FILE

```
tele-saham-bot/
├── bot.py                 # Main bot file
├── config.py              # Konfigurasi bot
├── database.py            # Handler database SQLite
├── saham_handler.py       # Handler data saham
├── ai_handler.py          # AI untuk tanya jawab
├── keep_alive.py          # Web server keep alive
├── requirements.txt       # Daftar dependencies
├── saham.sh               # Script installer
├── .env                   # File token (dibuat saat install)
├── saham_bot.db           # Database SQLite
└── bot.log                # File log
```

---

## 📄 DAFTAR FILE BOT

### **1. bot.py** (Main Bot)
File utama yang menjalankan bot Telegram. Mengatur semua handler, callback, dan routing pesan.

**Fungsi Utama:**
• Menu utama dengan inline keyboard
• Handler untuk /start
• Callback query handler untuk semua tombol
• Tanya AI handler
• Analisis saham handler
• Screening handler

### **2. config.py** (Konfigurasi)
File konfigurasi untuk menyimpan token dan pengaturan bot.

```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
BOT_USERNAME = os.getenv('BOT_USERNAME', '@NamaBotAnda')
DATABASE_NAME = 'saham_bot.db'

BOT_SETTINGS = {
    'max_watchlist': 10,
    'max_notifications': 5,
    'default_timeframe': '1D',
    'keep_alive': True
}
```

### **3. database.py** (Database Handler)
Mengelola database SQLite untuk menyimpan data user, watchlist, dan notifikasi.

**Tabel:**
• users - Data pengguna
• watchlist - Daftar pantauan
• notifications - Notifikasi harga
• price_history - Riwayat harga

### **4. saham_handler.py** (Handler Saham)
Mengelola data saham, analisis teknikal, dan screening.

**Fungsi:**
• `get_analisis(kode)` - Dapatkan analisis saham
• `get_ihsg()` - Data IHSG
• `get_screening(kategori)` - Screening berdasarkan kriteria
• Data dummy untuk pengembangan

### **5. ai_handler.py** (AI Handler)
Menjawab pertanyaan pengguna tentang saham.

**Topik:**
• RSI, MACD, Moving Average
• P/E Ratio, PBV, ROE
• Pola Double Bottom, Candlestick
• Strategi Day Trade, Swing Trade
• Analisis BBCA, TLKM, dll

### **6. keep_alive.py** (Web Server)
Menjalankan web server Flask agar bot tetap aktif di hosting gratis.

```python
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot Saham Telegram Aktif 24/7!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🌐 Web server started on port 8080")
```

### **7. requirements.txt** (Dependencies)
Daftar package Python yang diperlukan.

```
python-telegram-bot==20.7
requests==2.31.0
pandas==2.0.3
numpy==1.24.3
python-dotenv==1.0.0
flask==3.0.0
g4f==0.2.0
apscheduler==3.10.4
schedule==1.2.0
```

### **8. saham.sh** (Installer Script)
Script all-in-one untuk install, manage, dan maintain bot.

**Fitur Installer:**
• Cek OS (Ubuntu/Debian/Termux)
• Install dependencies otomatis
• Download semua file dari GitHub
• Setup token bot
• Install dengan Screen/Systemd/Tmux
• Menu manajemen (start, stop, restart)
• Backup & restore database
• Update bot
• Lihat log

---

## ⚙️ KONFIGURASI

### **MENDAPATKAN TOKEN BOT**
1. Buka Telegram, cari [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti petunjuk, beri nama bot
4. Dapatkan token (contoh: `7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)

### **FILE .ENV**
```env
BOT_TOKEN=7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
BOT_USERNAME=@NamaBotAnda
DATABASE_NAME=saham_bot.db
```

### **FILE CONFIG.PY**
```python
# Setting bot
BOT_SETTINGS = {
    'max_watchlist': 10,        # Maksimal watchlist per user
    'max_notifications': 5,      # Maksimal notifikasi
    'default_timeframe': '1D',   # Timeframe default chart
    'keep_alive': True           # Aktifkan web server
}
```

---

## 📊 COMMAND LIST

| Command | Deskripsi |
|---------|-----------|
| `/start` | Mulai bot, menu utama |
| `/help` | Bantuan |
| `/ai` | Tanya AI |
| `/ai [pertanyaan]` | Langsung tanya (contoh: `/ai apa itu rsi`) |
| `/analisis BBCA` | Analisis saham BBCA |
| `/ihsg` | Lihat IHSG |
| `/gainer` | Top gainer hari ini |
| `/loser` | Top loser hari ini |
| `/screening` | Menu screening |
| `/screening swing` | Screening swing trading |
| `/screening daytrade` | Screening day trade |
| `/watchlist` | Lihat watchlist |
| `/watchlist add BBCA` | Tambah BBCA ke watchlist |
| `/notifikasi` | Atur notifikasi |
| `/notifikasi BBCA 10000` | Notifikasi jika BBCA > 10000 |
| `/about` | Tentang bot |

---

## 🚨 TROUBLESHOOTING

### **1. BOT TIDAK MERESPON**

**Gejala:** Bot tidak membalas pesan, tidak muncul menu.

**Solusi:**
```bash
# Cek apakah bot berjalan
screen -ls
# atau
sudo systemctl status sahabot.service

# Cek log untuk melihat error
tail -f ~/tele-saham-bot/bot.log

# Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 ~/tele-saham-bot/bot.py
```

---

### **2. ERROR "MODULE NOT FOUND"**

**Gejala:** Muncul error `ModuleNotFoundError: No module named 'xxx'`

**Solusi:**
```bash
# Install semua dependencies
pip3 install -r ~/tele-saham-bot/requirements.txt

# Atau install manual
pip3 install python-telegram-bot requests pandas numpy python-dotenv flask g4f apscheduler schedule
```

---

### **3. TOKEN INVALID**

**Gejala:** Error `Unauthorized` atau `Token invalid` saat bot dijalankan.

**Penyebab:** Token bot salah atau sudah direset.

**Solusi:**
```bash
# 1. Cek token di @BotFather
# Buka Telegram > cari @BotFather > kirim /mybots > pilih bot Anda > pilih API Token

# 2. Edit file .env
cd ~/tele-saham-bot
nano .env

# 3. Perbaiki token
BOT_TOKEN=7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw

# 4. Simpan (Ctrl+X, Y, Enter)

# 5. Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py
```

**Cek Token:**
```bash
# Test token dengan curl
curl https://api.telegram.org/bot[TOKEN_ANDA]/getMe
# Contoh: curl https://api.telegram.org/bot7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw/getMe
```

---

### **4. PORT 8080 SUDAH DIGUNAKAN**

**Gejala:** Error `Address already in use` atau `Port 8080 already in use`.

**Solusi:**
```bash
# 1. Cek proses yang menggunakan port 8080
sudo lsof -i :8080
# atau
netstat -tlnp | grep 8080

# 2. Jika ada proses lain, matikan
sudo kill -9 [PID]  # Ganti [PID] dengan nomor proses

# 3. Atau ganti port di keep_alive.py
cd ~/tele-saham-bot
nano keep_alive.py

# Ubah baris: app.run(host='0.0.0.0', port=8080)
# Menjadi:  app.run(host='0.0.0.0', port=8081)

# 4. Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py
```

---

### **5. DATABASE ERROR**

**Gejala:** Error `sqlite3.OperationalError` atau `database disk image is malformed`.

**Solusi:**
```bash
# 1. Backup database yang rusak
cd ~/tele-saham-bot
cp saham_bot.db saham_bot_backup_$(date +%Y%m%d).db

# 2. Hapus database yang rusak
rm saham_bot.db

# 3. Restart bot (akan buat database baru)
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py

# 4. Jika ingin restore data dari backup
# (Hanya lakukan jika backup tidak rusak)
sqlite3 saham_bot_backup.db .dump | sqlite3 saham_bot.db
```

---

### **6. SCREEN ERROR**

**Gejala:** `Cannot open your terminal '/dev/pts/0'` atau screen tidak bisa diakses.

**Solusi:**
```bash
# 1. Install screen jika belum ada
sudo apt install screen -y

# 2. Kill semua session screen
screen -ls | grep Detached | cut -d. -f1 | awk '{print $1}' | xargs kill

# 3. Start ulang dengan screen baru
cd ~/tele-saham-bot
screen -dmS sahabot python3 bot.py

# 4. Cek apakah berjalan
screen -ls
# Harusnya ada: sahabot (Detached)

# 5. Masuk ke screen
screen -r sahabot
# Keluar: Ctrl+A lalu D
```

---

### **7. PERMISSION DENIED**

**Gejala:** Error `Permission denied` saat menjalankan script.

**Solusi:**
```bash
# Beri permission pada file
chmod +x ~/tele-saham-bot/saham.sh
chmod 755 ~/tele-saham-bot/bot.py
chmod 755 ~/tele-saham-bot/*.py

# Jika masih error, jalankan dengan sudo
sudo python3 bot.py
```

---

### **8. CONNECTION ERROR / TIMEOUT**

**Gejala:** Error `Timeout` atau `ConnectionError` saat bot mencoba mengakses API.

**Solusi:**
```bash
# 1. Cek koneksi internet
ping google.com

# 2. Cek firewall
sudo ufw status

# 3. Jika menggunakan proxy, nonaktifkan dulu
unset http_proxy
unset https_proxy

# 4. Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py
```

---

### **9. MEMORY ERROR / BOT CRASH**

**Gejala:** Bot tiba-tiba mati atau error `MemoryError`.

**Solusi:**
```bash
# 1. Cek penggunaan memory
free -h
top

# 2. Restart bot dengan memory limit
cd ~/tele-saham-bot
screen -dmS sahabot bash -c "ulimit -v 512000; python3 bot.py"

# 3. Tambahkan swap jika perlu
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### **10. LOG FILE TERLALU BESAR**

**Gejala:** File `bot.log` membesar hingga puluhan GB.

**Solusi:**
```bash
# 1. Cek ukuran log
du -sh ~/tele-saham-bot/bot.log

# 2. Backup log lama
mv ~/tele-saham-bot/bot.log ~/tele-saham-bot/bot_old.log

# 3. Buat log baru (otomatis)
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py

# 4. Atau buat log rotation (otomatis)
sudo nano /etc/logrotate.d/sahabot
```

Isi dengan:
```
/home/$USER/tele-saham-bot/bot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 $USER $USER
}
```

---

## 📝 LISENSI

MIT License

Copyright (c) 2026 Script-VIP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🤝 KONTAK & DUKUNGAN

- **GitHub**: [https://github.com/script-VIP/bott](https://github.com/script-VIP/bott)
- **Issues**: [https://github.com/script-VIP/bott/issues](https://github.com/script-VIP/bott/issues)
- **Telegram**: [@BotSupport](https://t.me/BotSupport)

---

### ⭐ BINTANGI REPOSITORI INI JIKA MEMBANTU!

```
███████╗███████╗██╗     ██╗███╗   ███╗ █████╗ ████████╗
██╔════╝██╔════╝██║     ██║████╗ ████║██╔══██╗╚══██╔══╝
███████╗█████╗  ██║     ██║██╔████╔██║███████║   ██║   
╚════██║██╔══╝  ██║     ██║██║╚██╔╝██║██╔══██║   ██║   
███████║███████╗███████╗██║██║ ╚═╝ ██║██║  ██║   ██║   
╚══════╝╚══════╝╚══════╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
```

**🚀 Selamat menggunakan Bot Saham Telegram Indonesia!**
```

---

## ✅ **README.md INI SUDAH LENGKAP DAN SIAP DI COPY!**

**Yang perlu Anda lakukan:**
1. **Copy semua teks di atas** (dari `# 🤖 BOT SAHAM...` sampai `🚀 Selamat menggunakan...`)
2. **Simpan sebagai file** `README.md`
3. **Upload ke GitHub** bersama file-file lainnya

**File sudah termasuk:**
- ✅ Link Install 1 Detik
- ✅ Fitur Lengkap (Tanya AI, Analisis, Screening)
- ✅ Screenshot
- ✅ Cara Install (3 Metode)
- ✅ Cara Upgrade
- ✅ Menjaga Bot 24/7 (4 Metode)
- ✅ Struktur File
- ✅ Daft#
