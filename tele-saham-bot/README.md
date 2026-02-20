```markdown
# 🤖 BOT SAHAM TELEGRAM INDONESIA

Bot Telegram untuk informasi saham Indonesia, analisis teknikal, screening, dan konsultasi AI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Telegram](https://img.shields.io/badge/telegram-bot-blue)
![License](https://img.shields.io/badge/license-MIT-orange)
![Ubuntu](https://img.shields.io/badge/ubuntu-18.04+-orange)
![Debian](https://img.shields.io/badge/debian-10+-red)

## 📋 DAFTAR ISI
- [🔗 Link Install](#-link-install)
- [✨ Fitur](#-fitur)
- [📸 Screenshot](#-screenshot)
- [🚀 Cara Install Lengkap](#-cara-install-lengkap)
- [🔄 Cara Upgrade](#-cara-upgrade)
- [⏰ Menjaga Bot Tetap Aktif 24/7](#-menjaga-bot-tetap-aktif-247)
- [📁 Struktur File](#-struktur-file)
- [⚙️ Konfigurasi](#-konfigurasi)
- [📊 Command List](#-command-list)
- [🚨 Troubleshooting](#-troubleshooting)
- [📝 Lisensi](#-lisensi)

## 🔗 LINK INSTALL

### **INSTALL 1 DETIK**
```bash
wget -O install.sh https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh && chmod +x install.sh && ./install.sh
```

### **DOWNLOAD MANUAL**
```bash
# Download script installer
wget https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh

# Beri permission
chmod +x saham.sh

# Jalankan
./saham.sh
```

### **REPOSITORY GITHUB**
```
https://github.com/script-VIP/bott
```

### **FILE RAW LINKS**
| File | Link Install |
|------|--------------|
| **Main Installer** | [`saham.sh`](https://raw.githubusercontent.com/script-VIP/bott/main/saham.sh) |
| Main Bot | [`bot.py`](https://raw.githubusercontent.com/script-VIP/bott/main/bot.py) |
| Konfigurasi | [`config.py`](https://raw.githubusercontent.com/script-VIP/bott/main/config.py) |
| Database | [`database.py`](https://raw.githubusercontent.com/script-VIP/bott/main/database.py) |
| Handler Saham | [`saham_handler.py`](https://raw.githubusercontent.com/script-VIP/bott/main/saham_handler.py) |
| AI Handler | [`ai_handler.py`](https://raw.githubusercontent.com/script-VIP/bott/main/ai_handler.py) |
| Keep Alive | [`keep_alive.py`](https://raw.githubusercontent.com/script-VIP/bott/main/keep_alive.py) |
| Dependencies | [`requirements.txt`](https://raw.githubusercontent.com/script-VIP/bott/main/requirements.txt) |
| Dokumentasi | [`README.md`](https://raw.githubusercontent.com/script-VIP/bott/main/README.md) |

## ✨ FITUR

### 🤖 TANYA AI SEPUTAR SAHAM
- Tanya tentang indikator teknikal (RSI, MACD, MA, dll)
- Tanya tentang fundamental (P/E, PBV, ROE)
- Tanya strategi trading (Day Trade, Swing, Long Term)
- Tanya analisis saham spesifik
- Edukasi saham untuk pemula

### 📈 ANALISIS SAHAM INDIVIDUAL
- Harga real-time
- Perubahan harga
- Signal Day Trade (entry, target 3 level, stop loss)
- Signal Swing Trading (entry, target 3 level, stop loss)
- Moving Average (MA5, MA10, MA20, MA50, MA100)
- Oscillator (RSI, MACD, Stochastic, CCI, Williams %R)
- Volume Analysis
- Bandarmology (Asing, Asing NG, Retail, Mutual)
- Support & Resistance (3 level)
- Risk Warning

### 📊 SCREENING SAHAM
- 🔥 Top Momentum
- 💡 Rebound Potential (Oversold)
- 💎 Bandar & Asing Akumulasi (1D/3D/5D)
- 🚀 Breakout & Resisten
- 🛡️ Area Support
- 🔄 Potensi Tutup Gap
- 🥈 Double Bottom
- ⬆️ On Pullback
- 📊 Swing Trading
- ⚡ Day Trade
- 📈 Long Term
- 📉 Open Low
- 📈 Open High

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

## 🚀 CARA INSTALL LENGKAP

### **PRASYARAT**
- Ubuntu 18.04+ / Debian 10+ / Termux (Android)
- Python 3.7+
- Token bot dari [@BotFather](https://t.me/BotFather)

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
- **Menu 1**: Install dengan Screen (mudah)
- **Menu 2**: Install dengan Systemd (rekomendasi 24/7)
- **Menu 3**: Install dengan Tmux (alternatif)

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
# Jika pake screen:
screen -X -S sahabot quit
screen -dmS sahabot python3 bot.py
```

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
```

### **METODE 4: AUTO RESTART DENGAN CRON**

```bash
# Buat cron job untuk cek setiap 5 menit
crontab -e

# Tambahkan baris ini:
*/5 * * * * pgrep -f "python3.*bot.py" || screen -dmS sahabot python3 /home/username/tele-saham-bot/bot.py
```

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

## ⚙️ KONFIGURASI

### **MENDAPATKAN TOKEN BOT**
1. Buka Telegram, cari [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti petunjuk, beri nama bot
4. Dapatkan token (contoh: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### **FILE .ENV**
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
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

## 📊 COMMAND LIST

| Command | Deskripsi |
|---------|-----------|
| `/start` | Mulai bot, menu utama |
| `/help` | Bantuan |
| `/ai` | Tanya AI |
| `/analisis BBCA` | Analisis saham BBCA |
| `/ihsg` | Lihat IHSG |
| `/gainer` | Top gainer hari ini |
| `/loser` | Top loser hari ini |
| `/screening` | Menu screening |
| `/watchlist` | Lihat watchlist |
| `/notifikasi` | Atur notifikasi |

## 🚨 TROUBLESHOOTING

### **BOT TIDAK MERESPON**
```bash
# Cek apakah bot berjalan
screen -ls
# atau
sudo systemctl status sahabot.service

# Cek log
tail -f ~/tele-saham-bot/bot.log

# Restart bot
screen -X -S sahabot quit
screen -dmS sahabot python3 ~/tele-saham-bot/bot.py
```

### **ERROR "MODULE NOT FOUND"**
```bash
pip3 install -r ~/tele-saham-bot/requirements.txt
```

### **TOKEN INVALID**
```bash
cd ~/tele-saham-bot
nano .env
# Perbaiki token
```

### **PORT 8080 SUDAH DIGUNAKAN**
```bash
# Ganti port di keep_alive.py
nano ~/tele-saham-bot/keep_alive.py
# Ubah port=8080 menjadi port=8081
```

### **DATABASE ERROR**
```bash
# Backup dulu
cp ~/tele-saham-bot/saham_bot.db ~/saham_bot_backup.db

# Hapus database
rm ~/tele-saham-bot/saham_bot.db

# Restart bot (akan buat database baru)
screen -X -S sahabot quit
screen -dmS sahabot python3 ~/tele-saham-bot/bot.py
```

## 📝 LISENSI

MIT License - Silakan gunakan, modifikasi, dan distribusikan.

## 🤝 KONTAK & DUKUNGAN

- **GitHub**: [https://github.com/script-VIP/bott](https://github.com/script-VIP/bott)
- **Report Issue**: [https://github.com/script-VIP/bott/issues](https://github.com/script-VIP/bott/issues)

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

Sekarang daftar isinya sudah bisa diklik (hyperlink) karena menggunakan format markdown yang benar:
- `[🔗 Link Install](#-link-install)` 
- `[✨ Fitur](#-fitur)`
- `[📸 Screenshot](#-screenshot)`
- Dan seteseterusn
