#!/bin/bash

# ================================================
# INSTALLER BOT VIP - TANPA INPUT ULANG
# LANGSUNG PAKAI .vars.json YANG SUDAH ADA
# ================================================

# Warna
green='\e[32m'
red='\e[31m'
yellow='\e[33m'
blue='\e[34m'
nc='\e[0m'

clear
echo -e "${blue}===============================================${nc}"
echo -e "${green}    INSTALLER BOT VIP - TANPA INPUT${nc}"
echo -e "${green}    (Pakai .vars.json yang sudah ada)${nc}"
echo -e "${blue}===============================================${nc}"
echo ""

# Cek root
if [[ $EUID -ne 0 ]]; then
   echo -e "${red}❌ Harus root!${nc}"
   exit 1
fi

# ================================================
# SET TIMEZONE
# ================================================
echo -e "${yellow}[1/6]⏳ Set timezone...${nc}"
timedatectl set-timezone Asia/Jakarta
echo -e "${green}✅ Done${nc}"
echo ""

# ================================================
# INSTALL DEPENDENCIES
# ================================================
echo -e "${yellow}[2/6]⏳ Install dependencies...${nc}"
apt update -y
apt install -y git curl wget jq nano sqlite3 nodejs npm
npm install -g npm@latest pm2
echo -e "${green}✅ Done${nc}"
echo ""

# ================================================
# CLONE REPOSITORY
# ================================================
echo -e "${yellow}[3/6]⏳ Clone repository...${nc}"
cd /root
rm -rf bott
git clone https://github.com/script-VIP/bott.git
cd bott/Botresseler
echo -e "${green}✅ Done${nc}"
echo ""

# ================================================
# CEK FILE .vars.json
# ================================================
echo -e "${yellow}[4/6]⏳ Memeriksa file .vars.json...${nc}"

if [ ! -f ".vars.json" ]; then
    echo -e "${red}❌ File .vars.json tidak ditemukan!${nc}"
    echo -e "${yellow}Silakan buat file .vars.json terlebih dahulu.${nc}"
    exit 1
else
    echo -e "${green}✅ File .vars.json ditemukan${nc}"
    # Tampilkan info tanpa token
    NAMA_STORE=$(jq -r '.NAMA_STORE' .vars.json)
    ADMIN_CONTACT=$(jq -r '.ADMIN_CONTACT' .vars.json)
    echo -e "  • Nama Store : ${green}$NAMA_STORE${nc}"
    echo -e "  • Admin      : ${green}$ADMIN_CONTACT${nc}"
fi
echo ""

# ================================================
# INSTALL NODE MODULES
# ================================================
echo -e "${yellow}[5/6]⏳ Install node modules...${nc}"
npm install
echo -e "${green}✅ Done${nc}"
echo ""

# ================================================
# JALANKAN BOT
# ================================================
echo -e "${yellow}[6/6]⏳ Menjalankan bot...${nc}"

# Buat folder logs
mkdir -p /root/bott/Botresseler/logs

# Kill pm2 lama
pm2 kill 2>/dev/null
rm -rf /root/.pm2 2>/dev/null

# Jalankan bot
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo -e "${green}✅ Bot berjalan!${nc}"
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
echo -e "  • Nama Store : ${green}$NAMA_STORE${nc}"
echo -e "  • Admin      : ${green}$ADMIN_CONTACT${nc}"
echo ""
echo -e "${yellow}📌 CEK STATUS:${nc}"
echo -e "  • ${green}pm2 list${nc}"
echo -e "  • ${green}pm2 logs botresseler${nc}"
echo ""
echo -e "${yellow}📌 AKSES BOT:${nc}"
echo -e "  • Buka Telegram"
echo -e "  • Ketik ${green}/start${nc}"
echo ""
echo -e "${blue}===============================================${nc}"
