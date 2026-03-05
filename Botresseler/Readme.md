

```markdown
# 🤖 Bot VPN Gabungan (VPN Biasa + ZIVPN UDP)

Bot Telegram otomatis untuk penjualan akun VPN dengan dukungan multi-server, sistem saldo, manajemen reseller, dan backup otomatis.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Node](https://img.shields.io/badge/node-20.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## ✨ **Fitur Utama**

### 🌐 **VPN Biasa**
- ✅ SSH/OpenVPN
- ✅ VMess
- ✅ VLess
- ✅ Trojan
- ✅ Create, Renew, Delete, Lock, Unlock
- ✅ Change Limit IP
- ✅ Trial Akun (1x/hari untuk member biasa)
- ✅ Fix Akun (Lock + Unlock otomatis)

### ⚡ **ZIVPN UDP**
- ✅ Create Akun ZIVPN
- ✅ Renew Akun
- ✅ Delete Akun
- ✅ Trial Akun (khusus ZIVPN)

### 💰 **Sistem Keuangan**
- ✅ Saldo user (disimpan di database)
- ✅ Topup Manual (via admin)
- ✅ Transaksi tercatat
- ✅ Harga per hari (otomatis hitung total)

### 👥 **Manajemen Reseller**
- ✅ Daftar reseller (file `ressel.db`)
- ✅ Server khusus reseller
- ✅ Harga spesial (min deposit berbeda)
- ✅ Fitur tambahan untuk reseller

### 📊 **Multi Server**
- ✅ Bisa tambah banyak server (SG-1, SG-2, INDO-1, dll)
- ✅ Pemisahan server VPN biasa dan ZIVPN
- ✅ Pagination daftar server
- ✅ Cek status server via bot

### 💾 **Backup Otomatis**
- ✅ Backup database setiap 6 jam (00:00, 06:00, 12:00, 18:00)
- ✅ Dikirim ke Telegram (chat pribadi atau grup)
- ✅ Backup lokal tersimpan 7 hari

### 🛡️ **Fitur Admin**
- ✅ Tambah/Hapus/Edit server
- ✅ Tambah saldo user
- ✅ Manajemen reseller (add, list, delete)
- ✅ Broadcast ke semua user
- ✅ Restart bot via menu
- ✅ Backup manual via command

---

## 🚀 **Link Instalasi**

### **Instalasi Otomatis (Recommended)**
```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1 && apt update -y && apt install -y git curl && curl -L -k -sS https://raw.githubusercontent.com/script-VIP/bott/main/Botresseler/install.sh -o install.sh && bash install.sh
```

### **Instalasi Manual**

#### 1. Clone Repository
```bash
git clone https://github.com/script-VIP/bott.git
cd bott/Botresseler
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Konfigurasi Bot
```bash
nano .vars.json
```
Isi dengan data Anda:
```json
{
  "BOT_TOKEN": "isi_token_dari_@BotFather",
  "USER_ID": "isi_id_telegram_admin",
  "NAMA_STORE": "AimanVPNExpress",
  "GROUP_ID": "isi_id_grup_notifikasi",
  "PORT": "6969",
  "ADMIN_CONTACT": "@AimanVpnExpress",
  "ADMIN_WA": "085940335000",
  "BACKUP_CHAT_ID": "isi_id_untuk_backup"
}
```

#### 4. Jalankan Bot dengan PM2
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

---

## 📖 **Cara Penggunaan**

### **Menu User (Member)**
| Perintah | Keterangan |
|----------|------------|
| `/start` atau `/menu` | Tampilkan menu utama |
| Klik tombol | Navigasi fitur |

### **Menu Admin**
| Perintah | Keterangan |
|----------|------------|
| `/admin` | Buka menu admin |
| `/addsaldo <user_id> <jumlah>` | Tambah saldo user |
| `/addserver` | Tambah server VPN biasa |
| `/addserver_zivpn` | Tambah server ZIVPN |
| `/addressel <user_id>` | Tambah reseller |
| `/delressel <user_id>` | Hapus reseller |
| `/listressel` | Lihat daftar reseller |
| `/broadcast <pesan>` | Kirim broadcast |
| `/backup` | Backup manual |
| `/hapuslog` | Hapus file log |

---

## 🗂️ **Struktur Folder**
```
Botresseler/
├── .vars.json                 # Konfigurasi bot
├── app.js                      # File utama
├── backup.sh                   # Script backup otomatis
├── cek-port.sh                 # Cek status server
├── ecosystem.config.js         # Konfigurasi PM2
├── package.json                # Dependencies
├── reseller.js                 # Manajemen reseller
├── modules/
│   ├── vpn/                    # Module VPN biasa
│   │   ├── create.js
│   │   ├── renew.js
│   │   ├── del.js
│   │   ├── lock.js
│   │   ├── unlock.js
│   │   ├── change-ip.js
│   │   ├── trial.js
│   │   └── checkconfig.js
│   └── zivpn/                   # Module ZIVPN UDP
│       ├── create.js
│       ├── renew.js
│       ├── del.js
│       └── trial.js
└── backups/                     # Folder backup lokal
```

---

## 🗄️ **Database Structure**

### Tabel `users`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | ID Telegram user |
| saldo | INTEGER | Saldo user |
| join_date | INTEGER | Timestamp join |

### Tabel `Server` (VPN Biasa)
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER | Primary key |
| domain | TEXT | Domain server |
| auth | TEXT | Token API |
| harga | INTEGER | Harga per hari |
| nama_server | TEXT | Nama server (🇸🇬 SG-1) |
| quota | INTEGER | Quota (GB) |
| iplimit | INTEGER | Limit IP |
| batas_create_akun | INTEGER | Maksimal akun |
| total_create_akun | INTEGER | Akun terbuat |
| is_reseller_only | INTEGER | 0=public, 1=reseller |
| type | TEXT | 'vpn' atau 'zivpn' |

### Tabel `ServerZiVPN`
| Kolom | Tipe | Keterangan |
|-------|------|------------|
| id | INTEGER | Primary key |
| domain | TEXT | Domain server |
| auth | TEXT | Token API |
| harga | INTEGER | Harga per hari |
| nama_server | TEXT | Nama server |
| batas_create_akun | INTEGER | Maksimal akun |
| total_create_akun | INTEGER | Akun terbuat |
| is_reseller_only | INTEGER | 0=public, 1=reseller |

---

## 🔧 **Cara Menambah Server**

### Via Menu Admin Bot
1. Ketik `/admin`
2. Klik **`➕ Tambah Server VPN`** atau **`➕ Tambah Server ZIVPN`**
3. Ikuti petunjuk

### Via SQLite (Terminal)
```bash
sqlite3 botresseler.db

-- Tambah server SG-1
INSERT INTO Server (domain, auth, harga, nama_server, quota, iplimit, batas_create_akun, total_create_akun, type) 
VALUES ('sg1.domain.com', 'token_anda', 1000, '🇸🇬 SG-1', 100, 3, 100, 0, 'vpn');

-- Tambah server BIZNET (ZIVPN)
INSERT INTO ServerZiVPN (domain, auth, harga, nama_server, batas_create_akun, total_create_akun, is_reseller_only) 
VALUES ('biznet.domain.com', 'token_anda', 1500, '⚡ BIZNET-1', 50, 0, 0);

.exit
```

---

## 🔄 **Update Bot**

```bash
cd /root/Botresseler
git pull
npm install
pm2 restart botresseler
```

---

## 📞 **Kontak & Support**

- **Telegram**: [@AimanVpnExpress](https://t.me/AimanVpnExpress)
- **WhatsApp**: 085940335000
- **Repository**: [https://github.com/script-VIP/bott](https://github.com/script-VIP/bott)

---

## 📸 **Screenshoot**

![Menu Utama](https://via.placeholder.com/400x600?text=Menu+Utama)
![Menu VPN](https://via.placeholder.com/400x600?text=Menu+VPN)
![Menu ZIVPN](https://via.placeholder.com/400x600?text=Menu+ZIVPN)

---

## ⚖️ **Lisensi**

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.

---

## 🙏 **Credit**

- **Author**: Aiman VPN Express
- **Base**: FighterTunnel & API Potato
- **Inspirasi**: ARI VPN STORE

---

**⭐ Jangan lupa kasih star di repository ini jika bermanfaat!**
```

---

## 📦 **File Installer (install.sh)**

Buat juga file `install.sh` untuk instalasi otomatis:

```bash
#!/bin/bash

# Warna
green='\e[32m'
red='\e[31m'
nc='\e[0m'

echo -e "${green}========================================${nc}"
echo -e "   INSTALLER BOT VPN GABUNGAN"
echo -e "${green}========================================${nc}"

# Set timezone
timedatectl set-timezone Asia/Jakarta

# Install dependencies
apt update -y
apt install -y git curl jq wget nodejs npm
npm install -g npm@latest pm2

# Clone repository
cd /root
if [ -d "bott" ]; then
    rm -rf bott
fi
git clone https://github.com/script-VIP/bott.git
cd bott/Botresseler

# Install node modules
npm install

# Konfigurasi .vars.json
echo -e "${green}Silakan isi konfigurasi bot:${nc}"
read -p "Masukkan BOT_TOKEN: " token
read -p "Masukkan USER_ID (admin): " userid
read -p "Masukkan NAMA_STORE: " namastore
read -p "Masukkan GROUP_ID (opsional): " groupid
read -p "Masukkan ADMIN_CONTACT (contoh: @username): " admincontact
read -p "Masukkan ADMIN_WA: " adminwa
read -p "Masukkan BACKUP_CHAT_ID: " backuptid

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

# Beri izin execute
chmod +x backup.sh cek-port.sh

# Jalankan dengan PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

echo -e "${green}========================================${nc}"
echo -e "✅ INSTALASI SELESAI!"
echo -e "📱 Buka bot Telegram Anda"
echo -e "🔍 Ketik /start untuk memulai"
echo -e "${green}========================================${nc}"
```

```bash
# Beri izin execute
chmod +x install.sh
```

---

## ✅ **Ringkasan File yang Perlu Diupload ke GitHub**

| File | Keterangan |
|------|------------|
| `Botresseler/.vars.json` | Template (isi manual) |
| `Botresseler/app.js` | File utama |
| `Botresseler/backup.sh` | Script backup |
| `Botresseler/cek-port.sh` | Cek server |
| `Botresseler/ecosystem.config.js` | Konfig PM2 |
| `Botresseler/package.json` | Dependencies |
| `Botresseler/reseller.js` | Manajemen reseller |
| `Botresseler/README.md` | Dokumentasi |
| `Botresseler/install.sh` | Installer otomatis |
| `Botresseler/modules/vpn/*` | Module VPN biasa |
| `Botresseler/modules/zivpn/*` | Module ZIVPN |


``
