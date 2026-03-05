#!/bin/bash

# ================================================
# INSTALLER BOT VPN GABUNGAN (VPN Biasa + ZIVPN UDP)
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
echo -e "${green}    VPN Biasa + ZIVPN UDP${nc}"
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
echo -e "${yellow}[1/8]⏳ Mengatur timezone ke Asia/Jakarta...${nc}"
timedatectl set-timezone Asia/Jakarta
echo -e "${green}✅ Timezone set ke Asia/Jakarta${nc}"
echo ""

# ================================================
# UPDATE & INSTALL DEPENDENCIES
# ================================================
echo -e "${yellow}[2/8]⏳ Mengupdate system dan install dependencies...${nc}"
apt update -y
apt upgrade -y
apt install -y git curl wget jq nano sqlite3 nodejs npm
echo -e "${green}✅ Dependencies installed${nc}"
echo ""

# ================================================
# INSTALL NODE JS 20
# ================================================
echo -e "${yellow}[3/8]⏳ Install Node.js 20...${nc}"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g npm@latest pm2
echo -e "${green}✅ Node.js $(node -v) installed${nc}"
echo ""

# ================================================
# CLONE REPOSITORY
# ================================================
echo -e "${yellow}[4/8]⏳ Clone repository dari GitHub...${nc}"
cd /root
if [ -d "bott" ]; then
    rm -rf bott
fi
git clone https://github.com/script-VIP/bott.git
cd bott/Botresseler
echo -e "${green}✅ Repository cloned${nc}"
echo ""

# ================================================
# INSTALL NODE MODULES
# ================================================
echo -e "${yellow}[5/8]⏳ Install Node.js dependencies...${nc}"
npm install
echo -e "${green}✅ Node modules installed${nc}"
echo ""

# ================================================
# KONFIGURASI .vars.json
# ================================================
echo -e "${yellow}[6/8]⏳ Konfigurasi bot...${nc}"
echo -e "${blue}Silakan isi data berikut:${nc}"
echo ""

read -p "Masukkan BOT_TOKEN (dari @BotFather) : " token
while [ -z "$token" ]; do
    echo -e "${red}❌ BOT_TOKEN tidak boleh kosong!${nc}"
    read -p "Masukkan BOT_TOKEN : " token
done

read -p "Masukkan USER_ID (admin) : " userid
while [ -z "$userid" ]; do
    echo -e "${red}❌ USER_ID tidak boleh kosong!${nc}"
    read -p "Masukkan USER_ID : " userid
done

read -p "Masukkan NAMA_STORE (contoh: AimanVPN) : " namastore
if [ -z "$namastore" ]; then
    namastore="AimanVPNExpress"
fi

read -p "Masukkan GROUP_ID (opsional, tekan Enter jika tidak ada) : " groupid
if [ -z "$groupid" ]; then
    groupid="0"
fi

read -p "Masukkan ADMIN_CONTACT (contoh: @AimanVpnExpress) : " admincontact
if [ -z "$admincontact" ]; then
    admincontact="@AimanVpnExpress"
fi

read -p "Masukkan ADMIN_WA (contoh: 085940335000) : " adminwa
if [ -z "$adminwa" ]; then
    adminwa="085940335000"
fi

read -p "Masukkan BACKUP_CHAT_ID (ID Telegram untuk backup) : " backuptid
while [ -z "$backuptid" ]; do
    echo -e "${red}❌ BACKUP_CHAT_ID tidak boleh kosong!${nc}"
    read -p "Masukkan BACKUP_CHAT_ID : " backuptid
done

# Buat file .vars.json
cat > .vars.json <<EOF
{
  "BOT_TOKEN": "$token",
  "USER_ID": "$userid",
  "NAMA_STORE": "$namastore",
  "GROUP_ID": "$groupid",
  "PORT": "6969",
  "ADMIN_CONTACT": "$admincontact",
  "ADMIN_WA": "$adminwa",
  "BACKUP_CHAT_ID": "$backuptid"
}
EOF

echo -e "${green}✅ Konfigurasi selesai${nc}"
echo ""

# ================================================
# SET PERMISSION
# ================================================
echo -e "${yellow}[7/8]⏳ Mengatur permission file...${nc}"
chmod +x backup.sh
chmod +x cek-port.sh
chmod +x install.sh
echo -e "${green}✅ Permission set${nc}"
echo ""

# ================================================
# JALANKAN BOT DENGAN PM2
# ================================================
echo -e "${yellow}[8/8]⏳ Menjalankan bot dengan PM2...${nc}"
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo -e "${green}✅ Bot berjalan dengan PM2${nc}"
echo ""

# ================================================
# SETUP BACKUP OTOMATIS (CRON)
# ================================================
echo -e "${yellow}⏳ Setup backup otomatis setiap 6 jam...${nc}"
(crontab -l 2>/dev/null; echo "0 */6 * * * /usr/bin/bash /root/bott/Botresseler/backup.sh") | crontab -
echo -e "${green}✅ Backup otomatis dijadwalkan setiap 6 jam (00:00, 06:00, 12:00, 18:00)${nc}"
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
echo -e "  • Nama Store : ${green}$namastore${nc}"
echo -e "  • Admin      : ${green}$admincontact${nc}"
echo -e "  • Backup ke  : ${green}$backuptid${nc}"
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
echo -e "${yellow}📌 ATAU VIA SQLITE:${nc}"
echo -e "  • ${green}cd /root/bott/Botresseler${nc}"
echo -e "  • ${green}sqlite3 botresseler.db${nc}"
echo -e "  • ${green}INSERT INTO Server ...${nc}"
echo ""
echo -e "${blue}===============================================${nc}"
echo -e "${green}✨ Terima kasih telah menggunakan installer ini!${nc}"
echo -e "${blue}===============================================${nc}"
