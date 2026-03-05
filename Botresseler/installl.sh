#!/bin/bash

# ================================================
# INSTALLER BOT VPN GABUNGAN (TANPA INPUT ULANG)
# ================================================

# Warna
green='\e[32m'
red='\e[31m'
yellow='\e[33m'
blue='\e[34m'
nc='\e[0m'

# Header
clear
echo -e "${blue}===============================================${nc}"
echo -e "${green}    INSTALLER BOT VPN GABUNGAN v1.0${nc}"
echo -e "${green}    (Tanpa Input Ulang - Pakai .vars.json)${nc}"
echo -e "${blue}===============================================${nc}"
echo ""

# Cek user root
if [[ $EUID -ne 0 ]]; then
   echo -e "${red}❌ Script ini harus dijalankan sebagai root!${nc}" 
   exit 1
fi

# ================================================
# SET TIMEZONE
# ================================================
echo -e "${yellow}[1/7]⏳ Mengatur timezone ke Asia/Jakarta...${nc}"
timedatectl set-timezone Asia/Jakarta
echo -e "${green}✅ Timezone set ke Asia/Jakarta${nc}"
echo ""

# ================================================
# UPDATE & INSTALL DEPENDENCIES
# ================================================
echo -e "${yellow}[2/7]⏳ Mengupdate system dan install dependencies...${nc}"
apt update -y
apt upgrade -y
apt install -y git curl wget jq nano sqlite3 nodejs npm
echo -e "${green}✅ Dependencies installed${nc}"
echo ""

# ================================================
# INSTALL NODE JS 20
# ================================================
echo -e "${yellow}[3/7]⏳ Install Node.js 20...${nc}"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g npm@latest pm2
echo -e "${green}✅ Node.js $(node -v) installed${nc}"
echo ""

# ================================================
# CEK FILE .vars.json
# ================================================
echo -e "${yellow}[4/7]⏳ Memeriksa file .vars.json...${nc}"
if [ ! -f ".vars.json" ]; then
    echo -e "${red}❌ File .vars.json tidak ditemukan!${nc}"
    echo -e "${yellow}Silakan buat file .vars.json terlebih dahulu.${nc}"
    exit 1
else
    echo -e "${green}✅ File .vars.json ditemukan${nc}"
    # Tampilkan isi .vars.json (sensor token)
    echo -e "${blue}Isi konfigurasi:${nc}"
    cat .vars.json | jq '."BOT_TOKEN" = "***HIDDEN***"'
fi
echo ""

# ================================================
# INSTALL NODE MODULES
# ================================================
echo -e "${yellow}[5/7]⏳ Install Node.js dependencies...${nc}"
npm install
echo -e "${green}✅ Node modules installed${nc}"
echo ""

# ================================================
# SET PERMISSION
# ================================================
echo -e "${yellow}[6/7]⏳ Mengatur permission file...${nc}"
if [ -f "backup.sh" ]; then
    chmod +x backup.sh
    echo -e "${green}✅ backup.sh${nc}"
fi
if [ -f "cek-port.sh" ]; then
    chmod +x cek-port.sh
    echo -e "${green}✅ cek-port.sh${nc}"
fi
echo ""

# ================================================
# JALANKAN BOT DENGAN PM2
# ================================================
echo -e "${yellow}[7/7]⏳ Menjalankan bot dengan PM2...${nc}"
pm2 delete botresseler 2>/dev/null
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo -e "${green}✅ Bot berjalan dengan PM2${nc}"
echo ""

# ================================================
# SETUP BACKUP OTOMATIS (CRON)
# ================================================
if [ -f "backup.sh" ]; then
    echo -e "${yellow}⏳ Setup backup otomatis setiap 6 jam...${nc}"
    (crontab -l 2>/dev/null | grep -v "backup.sh"; echo "0 */6 * * * /usr/bin/bash $(pwd)/backup.sh") | crontab -
    echo -e "${green}✅ Backup otomatis dijadwalkan setiap 6 jam${nc}"
fi
echo ""

# ================================================
# SELESAI
# ================================================
clear
echo -e "${blue}===============================================${nc}"
echo -e "${green}         INSTALASI SELESAI! 🎉${nc}"
echo -e "${blue}===============================================${nc}"
echo ""
echo -e "${yellow}📌 INFORMASI BOT:${nc}"
NAMA_STORE=$(jq -r '.NAMA_STORE' .vars.json)
ADMIN_CONTACT=$(jq -r '.ADMIN_CONTACT' .vars.json)
BACKUP_CHAT_ID=$(jq -r '.BACKUP_CHAT_ID' .vars.json)
echo -e "  • Nama Store : ${green}$NAMA_STORE${nc}"
echo -e "  • Admin      : ${green}$ADMIN_CONTACT${nc}"
echo -e "  • Backup ke  : ${green}$BACKUP_CHAT_ID${nc}"
echo ""
echo -e "${yellow}📌 CEK STATUS BOT:${nc}"
echo -e "  • ${green}pm2 list${nc} - Lihat status bot"
echo -e "  • ${green}pm2 logs botresseler${nc} - Lihat log"
echo -e "  • ${green}pm2 restart botresseler${nc} - Restart bot"
echo ""
echo -e "${yellow}📌 AKSES BOT:${nc}"
echo -e "  • Buka Telegram"
echo -e "  • Cari bot Anda"
echo -e "  • Ketik ${green}/start${nc}"
echo ""
echo -e "${yellow}📌 TAMBAH SERVER PERTAMA:${nc}"
echo -e "  • Ketik ${green}/admin${nc} di bot"
echo -e "  • Pilih ${green}➕ Tambah Server VPN${nc}"
echo -e "  • Ikuti petunjuk"
echo ""
echo -e "${blue}===============================================${nc}"
echo -e "${green}✨ Terima kasih telah menggunakan installer ini!${nc}"
echo -e "${blue}===============================================${nc}"
