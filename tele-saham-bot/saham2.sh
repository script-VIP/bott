#!/bin/bash

# ============================================
# AUTO INSTALLER BOT SAHAM TELEGRAM
# Ubuntu/Debian - 24/7 Auto Alive
# Support: Screen, Systemd, Tmux
# ============================================

# Warna output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# ============================================
# VARIABEL
# ============================================
BOT_DIR="$HOME/tele-saham-bot"
REPO_URL="https://raw.githubusercontent.com/script-VIP/bott/main"

# ============================================
# FUNGSI BANNER
# ============================================
print_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║     🤖 BOT SAHAM TELEGRAM - UBUNTU/DEBIAN INSTALLER        ║"
    echo "║                                                              ║"
    echo "║            Auto Alive 24/7 - Screen + Systemd               ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ============================================
# FUNGSI CEK DAN INSTALL DEPENDENCIES
# ============================================
install_dependencies() {
    echo -e "${YELLOW}[1/6] Menginstall dependencies...${NC}"
    
    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y python3 python3-pip python3-venv git screen tmux wget curl nano
    
    pip3 install --upgrade pip
    pip3 install python-telegram-bot requests pandas numpy python-dotenv flask g4f apscheduler schedule
    
    echo -e "${GREEN}✓ Dependencies selesai diinstall${NC}"
}

# ============================================
# FUNGSI DOWNLOAD FILE DARI GITHUB
# ============================================
download_files() {
    echo -e "${YELLOW}[2/6] Mendownload file bot dari repository...${NC}"
    
    # Buat folder
    mkdir -p $BOT_DIR
    cd $BOT_DIR
    
    # Download file dari GitHub
    echo -e "${BLUE}   Downloading bot.py...${NC}"
    wget -q ${REPO_URL}/bot.py -O bot.py || curl -fsSL ${REPO_URL}/bot.py -o bot.py
    
    echo -e "${BLUE}   Downloading config.py...${NC}"
    wget -q ${REPO_URL}/config.py -O config.py || curl -fsSL ${REPO_URL}/config.py -o config.py
    
    echo -e "${BLUE}   Downloading database.py...${NC}"
    wget -q ${REPO_URL}/database.py -O database.py || curl -fsSL ${REPO_URL}/database.py -o database.py
    
    echo -e "${BLUE}   Downloading saham_handler.py...${NC}"
    wget -q ${REPO_URL}/saham_handler.py -O saham_handler.py || curl -fsSL ${REPO_URL}/saham_handler.py -o saham_handler.py
    
    echo -e "${BLUE}   Downloading ai_handler.py...${NC}"
    wget -q ${REPO_URL}/ai_handler.py -O ai_handler.py || curl -fsSL ${REPO_URL}/ai_handler.py -o ai_handler.py
    
    echo -e "${BLUE}   Downloading keep_alive.py...${NC}"
    wget -q ${REPO_URL}/keep_alive.py -O keep_alive.py || curl -fsSL ${REPO_URL}/keep_alive.py -o keep_alive.py
    
    echo -e "${BLUE}   Downloading requirements.txt...${NC}"
    wget -q ${REPO_URL}/requirements.txt -O requirements.txt || curl -fsSL ${REPO_URL}/requirements.txt -o requirements.txt
    
    echo -e "${GREEN}✓ Semua file berhasil didownload${NC}"
}

# ============================================
# FUNGSI SETUP TOKEN
# ============================================
setup_token() {
    echo -e "${YELLOW}[3/6] Konfigurasi bot...${NC}"
    
    # Minta token dari user
    echo -e "${PURPLE}════════════════════════════════════════════${NC}"
    echo -e "${CYAN}🔑 Masukkan BOT TOKEN dari @BotFather${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════${NC}"
    read -p "Bot Token: " BOT_TOKEN
    
    # Buat file .env
    cat > $BOT_DIR/.env << EOF
BOT_TOKEN=$BOT_TOKEN
BOT_USERNAME=@NamaBotAnda
DATABASE_NAME=saham_bot.db
EOF
    
    echo -e "${GREEN}✓ Token berhasil disimpan${NC}"
}

# ============================================
# FUNGSI INSTALL DENGAN SCREEN
# ============================================
install_with_screen() {
    echo -e "${YELLOW}[4/6] Menjalankan bot dengan Screen...${NC}"
    
    cd $BOT_DIR
    
    # Kill screen session lama jika ada
    screen -X -S sahabot quit >/dev/null 2>&1
    
    # Jalankan di screen baru
    screen -dmS sahabot bash -c "cd $BOT_DIR && python3 bot.py"
    
    # Cek status
    sleep 3
    if screen -list | grep -q "sahabot"; then
        echo -e "${GREEN}✓ Bot berjalan dengan Screen (Session: sahabot)${NC}"
        echo -e "${BLUE}   • Lihat log: tail -f $BOT_DIR/bot.log${NC}"
        echo -e "${BLUE}   • Masuk screen: screen -r sahabot${NC}"
        echo -e "${BLUE}   • Keluar screen: Ctrl+A lalu D${NC}"
        echo -e "${BLUE}   • Matikan bot: screen -X -S sahabot quit${NC}"
    else
        echo -e "${RED}✗ Bot gagal berjalan${NC}"
    fi
}

# ============================================
# FUNGSI INSTALL DENGAN SYSTEMD
# ============================================
install_with_systemd() {
    echo -e "${YELLOW}[4/6] Menjalankan bot dengan Systemd...${NC}"
    
    cd $BOT_DIR
    
    # Buat service file
    sudo bash -c "cat > /etc/systemd/system/sahabot.service << EOF
[Unit]
Description=Telegram Saham Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_DIR
ExecStart=/usr/bin/python3 $BOT_DIR/bot.py
Restart=always
RestartSec=10
StandardOutput=append:$BOT_DIR/bot.log
StandardError=append:$BOT_DIR/bot.log

[Install]
WantedBy=multi-user.target
EOF"
    
    # Reload systemd dan start service
    sudo systemctl daemon-reload
    sudo systemctl enable sahabot.service
    sudo systemctl start sahabot.service
    
    # Cek status
    sleep 3
    if sudo systemctl is-active --quiet sahabot.service; then
        echo -e "${GREEN}✓ Bot berjalan dengan Systemd${NC}"
        echo -e "${BLUE}   • Cek status: sudo systemctl status sahabot.service${NC}"
        echo -e "${BLUE}   • Lihat log: sudo journalctl -u sahabot.service -f${NC}"
        echo -e "${BLUE}   • Restart: sudo systemctl restart sahabot.service${NC}"
        echo -e "${BLUE}   • Stop: sudo systemctl stop sahabot.service${NC}"
    else
        echo -e "${RED}✗ Bot gagal berjalan${NC}"
    fi
}

# ============================================
# FUNGSI INSTALL DENGAN TMUX
# ============================================
install_with_tmux() {
    echo -e "${YELLOW}[4/6] Menjalankan bot dengan Tmux...${NC}"
    
    cd $BOT_DIR
    
    # Kill tmux session lama jika ada
    tmux kill-session -t sahabot >/dev/null 2>&1
    
    # Jalankan di tmux baru
    tmux new-session -d -s sahabot "cd $BOT_DIR && python3 bot.py"
    
    # Cek status
    sleep 3
    if tmux has-session -t sahabot 2>/dev/null; then
        echo -e "${GREEN}✓ Bot berjalan dengan Tmux (Session: sahabot)${NC}"
        echo -e "${BLUE}   • Lihat log: tail -f $BOT_DIR/bot.log${NC}"
        echo -e "${BLUE}   • Masuk tmux: tmux attach -t sahabot${NC}"
        echo -e "${BLUE}   • Keluar tmux: Ctrl+B lalu D${NC}"
        echo -e "${BLUE}   • Matikan bot: tmux kill-session -t sahabot${NC}"
    else
        echo -e "${RED}✗ Bot gagal berjalan${NC}"
    fi
}

# ============================================
# FUNGSI CEK STATUS
# ============================================
check_status() {
check_status() {
    echo -e "${YELLOW}[5/6] Memeriksa status bot...${NC}"
    
    # Cek proses
    if screen -list | grep -q "sahabot"; then
        echo -e "${GREEN}✓ Bot aktif (Screen)${NC}"
        BOT_ACTIVE=1
    elif tmux has-session -t sahabot 2>/dev/null; then
        echo -e "${GREEN}✓ Bot aktif (Tmux)${NC}"
        BOT_ACTIVE=1
    elif sudo systemctl is-active --quiet sahabot.service 2>/dev/null; then
        echo -e "${GREEN}✓ Bot aktif (Systemd)${NC}"
        BOT_ACTIVE=1
    else
        echo -e "${RED}✗ Bot tidak aktif${NC}"
        BOT_ACTIVE=0
    fi
    
    # CEK PORT 8080 - VERSI ROBUST (TIDAK PERLU NETSTAT)
    echo -e "${YELLOW}   Memeriksa web server...${NC}"
    
    # Method 1: Pakai curl (paling akurat)
    if command -v curl &> /dev/null; then
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Web server aktif di port 8080 (merespon)${NC}"
            WEB_ACTIVE=1
        else
            # Method 2: Pakai lsof kalau curl gagal
            if command -v lsof &> /dev/null; then
                if lsof -i :8080 | grep -q LISTEN; then
                    echo -e "${GREEN}✓ Web server aktif di port 8080 (lsof)${NC}"
                    WEB_ACTIVE=1
                else
                    echo -e "${RED}✗ Web server tidak aktif${NC}"
                    WEB_ACTIVE=0
                fi
            # Method 3: Pakai ss kalau ada
            elif command -v ss &> /dev/null; then
                if ss -tln | grep -q ":8080"; then
                    echo -e "${GREEN}✓ Web server aktif di port 8080 (ss)${NC}"
                    WEB_ACTIVE=1
                else
                    echo -e "${RED}✗ Web server tidak aktif${NC}"
                    WEB_ACTIVE=0
                fi
            # Method 4: Pakai netstat kalau ada
            elif command -v netstat &> /dev/null; then
                if netstat -tln | grep -q ":8080 "; then
                    echo -e "${GREEN}✓ Web server aktif di port 8080 (netstat)${NC}"
                    WEB_ACTIVE=1
                else
                    echo -e "${RED}✗ Web server tidak aktif${NC}"
                    WEB_ACTIVE=0
                fi
            else
                echo -e "${YELLOW}⚠️ Tidak bisa cek port (install net-tools atau lsof)${NC}"
                echo -e "${YELLOW}   Tapi bot kemungkinan tetap berjalan${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}⚠️ curl tidak tersedia, gunakan metode alternatif${NC}"
        # Fallback ke lsof
        if command -v lsof &> /dev/null; then
            if lsof -i :8080 | grep -q LISTEN; then
                echo -e "${GREEN}✓ Web server aktif di port 8080${NC}"
            else
                echo -e "${YELLOW}⚠️ Web server mungkin tidak aktif${NC}"
            fi
        fi
    fi
    
    # Beri rekomendasi
    if [ $BOT_ACTIVE -eq 1 ]; then
        echo -e "${GREEN}✅ Bot berjalan normal${NC}"
        echo -e "${BLUE}   • Lihat log: tail -f ~/tele-saham-bot/bot.log${NC}"
        echo -e "${BLUE}   • Buka web: http://localhost:8080${NC}"
    fi
}
# ============================================
# FUNGSI LIHAT LOG
# ============================================
view_logs() {
    echo -e "${YELLOW}[6/6] Menampilkan log bot...${NC}"
    echo -e "${BLUE}Tekan Ctrl+C untuk keluar dari log${NC}"
    sleep 2
    tail -f $BOT_DIR/bot.log
}

# ============================================
# FUNGSI MENU UTAMA
# ============================================
show_menu() {
    echo -e "\n${CYAN}════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}📋 MENU BOT SAHAM${NC}"
    echo -e "${CYAN}════════════════════════════════════════════${NC}"
    echo -e "${GREEN}1.${NC} Install Bot Baru (Screen)"
    echo -e "${GREEN}2.${NC} Install Bot Baru (Systemd - Recomended)"
    echo -e "${GREEN}3.${NC} Install Bot Baru (Tmux)"
    echo -e "${GREEN}4.${NC} Start Bot"
    echo -e "${GREEN}5.${NC} Stop Bot"
    echo -e "${GREEN}6.${NC} Restart Bot"
    echo -e "${GREEN}7.${NC} Cek Status"
    echo -e "${GREEN}8.${NC} Lihat Log"
    echo -e "${GREEN}9.${NC} Update Bot (Download ulang file)"
    echo -e "${GREEN}10.${NC} Backup Database"
    echo -e "${GREEN}11.${NC} Restore Database"
    echo -e "${GREEN}12.${NC} Uninstall Bot"
    echo -e "${GREEN}0.${NC} Keluar"
    echo -e "${CYAN}════════════════════════════════════════════${NC}"
    read -p "Pilih menu [0-12]: " MENU_CHOICE
    
    case $MENU_CHOICE in
        1)
            install_dependencies
            download_files
            setup_token
            install_with_screen
            check_status
            ;;
        2)
            install_dependencies
            download_files
            setup_token
            install_with_systemd
            check_status
            ;;
        3)
            install_dependencies
            download_files
            setup_token
            install_with_tmux
            check_status
            ;;
        4)
            echo -e "${YELLOW}Starting bot...${NC}"
            if screen -list | grep -q "sahabot"; then
                echo -e "${GREEN}Bot sudah berjalan${NC}"
            else
                cd $BOT_DIR
                screen -dmS sahabot python3 bot.py
                echo -e "${GREEN}Bot started${NC}"
            fi
            ;;
        5)
            echo -e "${YELLOW}Stopping bot...${NC}"
            screen -X -S sahabot quit >/dev/null 2>&1
            tmux kill-session -t sahabot >/dev/null 2>&1
            sudo systemctl stop sahabot.service >/dev/null 2>&1
            echo -e "${GREEN}Bot stopped${NC}"
            ;;
        6)
            echo -e "${YELLOW}Restarting bot...${NC}"
            screen -X -S sahabot quit >/dev/null 2>&1
            tmux kill-session -t sahabot >/dev/null 2>&1
            sudo systemctl stop sahabot.service >/dev/null 2>&1
            sleep 2
            cd $BOT_DIR
            screen -dmS sahabot python3 bot.py
            echo -e "${GREEN}Bot restarted${NC}"
            ;;
        7)
            check_status
            ;;
        8)
            view_logs
            ;;
        9)
            echo -e "${YELLOW}Updating bot files...${NC}"
            download_files
            echo -e "${GREEN}Update selesai. Restart bot untuk menerapkan perubahan.${NC}"
            ;;
        10)
            cd $BOT_DIR
            cp saham_bot.db saham_bot_backup_$(date +%Y%m%d_%H%M%S).db
            echo -e "${GREEN}Backup database created${NC}"
            ;;
        11)
            cd $BOT_DIR
            ls -la saham_bot_backup*.db 2>/dev/null
            read -p "Masukkan nama file backup: " BACKUP_FILE
            if [[ -f "$BACKUP_FILE" ]]; then
                cp "$BACKUP_FILE" saham_bot.db
                echo -e "${GREEN}Database restored from $BACKUP_FILE${NC}"
            else
                echo -e "${RED}File tidak ditemukan${NC}"
            fi
            ;;
        12)
            read -p "Yakin ingin uninstall? (y/n): " CONFIRM
            if [[ "$CONFIRM" == "y" ]]; then
                screen -X -S sahabot quit >/dev/null 2>&1
                tmux kill-session -t sahabot >/dev/null 2>&1
                sudo systemctl stop sahabot.service >/dev/null 2>&1
                sudo systemctl disable sahabot.service >/dev/null 2>&1
                cd $HOME
                rm -rf $BOT_DIR
                echo -e "${GREEN}Bot dihapus${NC}"
                exit 0
            fi
            ;;
        0)
            echo -e "${GREEN}Terima kasih!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Pilihan tidak valid${NC}"
            ;;
    esac
}

# ============================================
# MAIN PROGRAM
# ============================================
print_banner

# Loop menu
while true; do
    show_menu
    echo -e "\n${YELLOW}Tekan Enter untuk kembali ke menu...${NC}"
    read
done
