const os = require('os');
const sqlite3 = require('sqlite3').verbose();
const express = require('express');
const { Telegraf, Markup } = require('telegraf');
const app = express();
const axios = require('axios');
const { isUserReseller, addReseller, removeReseller, listResellersSync } = require('./reseller');
const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');
const winston = require('winston');

// ================= LOGGER =================
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => {
      return `${timestamp} [${level.toUpperCase()}]: ${message}`;
    })
  ),
  transports: [
    new winston.transports.File({ filename: 'bot-error.log', level: 'error' }),
    new winston.transports.File({ filename: 'bot-combined.log' }),
  ],
});
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple(),
  }));
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ================= LOAD VARS =================
const vars = JSON.parse(fs.readFileSync('./.vars.json', 'utf8'));
const BOT_TOKEN = vars.BOT_TOKEN;
const port = vars.PORT || 6969;
const ADMIN = vars.USER_ID;
const adminIds = ADMIN.toString(); // Pastikan string
// atau langsung
const adminIds = "6198984094"; // PAKSA dengan ID langsung
const NAMA_STORE = vars.NAMA_STORE || 'AimanVPNExpress';
const GROUP_ID = vars.GROUP_ID;
const ADMIN_CONTACT = vars.ADMIN_CONTACT || '@AimanVpnExpress';
const ADMIN_WA = vars.ADMIN_WA || '085940335000';
const BACKUP_CHAT_ID = vars.BACKUP_CHAT_ID;

const bot = new Telegraf(BOT_TOKEN);
const adminIds = ADMIN;

// ================= DATABASE =================
const db = new sqlite3.Database('./botresseler.db', (err) => {
  if (err) {
    logger.error('Kesalahan koneksi SQLite3:', err.message);
  } else {
    logger.info('Terhubung ke SQLite3');
    initDatabase();
  }
});

function initDatabase() {
  // Tabel users
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    saldo INTEGER DEFAULT 0,
    join_date INTEGER
  )`);

  // Tabel server (untuk VPN biasa)
  db.run(`CREATE TABLE IF NOT EXISTS Server (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT,
    auth TEXT,
    harga INTEGER,
    nama_server TEXT,
    quota INTEGER,
    iplimit INTEGER,
    batas_create_akun INTEGER,
    total_create_akun INTEGER,
    is_reseller_only INTEGER DEFAULT 0,
    type TEXT DEFAULT 'vpn'  -- 'vpn' atau 'zivpn'
  )`);

  // Tabel server ZIVPN (terpisah atau pakai Server dengan type='zivpn')
  db.run(`CREATE TABLE IF NOT EXISTS ServerZiVPN (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT,
    auth TEXT,
    harga INTEGER,
    nama_server TEXT,
    quota INTEGER DEFAULT 0,
    iplimit INTEGER DEFAULT 0,
    batas_create_akun INTEGER,
    total_create_akun INTEGER,
    is_reseller_only INTEGER DEFAULT 0
  )`);

  // Tabel pending_deposits (tidak dipakai karena topup manual, tapi disimpan untuk kompatibilitas)
  db.run(`CREATE TABLE IF NOT EXISTS pending_deposits (
    unique_code TEXT PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    original_amount INTEGER,
    timestamp INTEGER,
    status TEXT,
    qr_message_id INTEGER
  )`);

  // Tabel transactions
  db.run(`CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount INTEGER,
    type TEXT,
    reference_id TEXT,
    timestamp INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
  )`);

  // Tabel trial access
  db.run(`CREATE TABLE IF NOT EXISTS trial_access (
    user_id INTEGER PRIMARY KEY,
    last_trial_date TEXT,
    trial_count INTEGER DEFAULT 0
  )`);
}

// ================= IMPORT MODULES VPN =================
const vpnCreate = require('./modules/vpn/create');
const vpnRenew = require('./modules/vpn/renew');
const vpnDel = require('./modules/vpn/del');
const vpnLock = require('./modules/vpn/lock');
const vpnUnlock = require('./modules/vpn/unlock');
const vpnChangeIp = require('./modules/vpn/change-ip');
const vpnTrial = require('./modules/vpn/trial');
const vpnCheck = require('./modules/vpn/checkconfig');

// ================= IMPORT MODULES ZIVPN =================
const ziCreate = require('./modules/zivpn/create');
const ziRenew = require('./modules/zivpn/renew');
const ziDel = require('./modules/zivpn/del');
const ziTrial = require('./modules/zivpn/trial');

// ================= STATE MANAGEMENT =================
const userState = {};

// ================= FILE PATHS =================
const trialFile = path.join(__dirname, 'trial.db');
const resselFilePath = path.join(__dirname, 'ressel.db');

// ================= HELPER FUNCTIONS =================
async function checkTrialAccess(userId) {
  return new Promise((resolve) => {
    const today = new Date().toISOString().slice(0, 10);
    db.get('SELECT last_trial_date FROM trial_access WHERE user_id = ?', [userId], (err, row) => {
      if (err || !row) return resolve(false);
      resolve(row.last_trial_date === today);
    });
  });
}

async function saveTrialAccess(userId) {
  const today = new Date().toISOString().slice(0, 10);
  db.run('INSERT OR REPLACE INTO trial_access (user_id, last_trial_date, trial_count) VALUES (?, ?, COALESCE((SELECT trial_count + 1 FROM trial_access WHERE user_id = ?), 1))',
    [userId, today, userId]);
}

const { isUserReseller } = require('./reseller');

// ================= COMMANDS =================
bot.command(['start', 'menu'], async (ctx) => {
  const userId = ctx.from.id;
  
  // Register user if not exists
  db.get('SELECT * FROM users WHERE user_id = ?', [userId], (err, row) => {
    if (!row) {
      db.run('INSERT INTO users (user_id, join_date) VALUES (?, ?)', [userId, Date.now()]);
    }
  });

  await sendMainMenu(ctx);
});

bot.command('admin', async (ctx) => {
  if (!adminIds.includes(ctx.from.id)) {
    return ctx.reply('🚫 Anda tidak memiliki izin untuk mengakses menu admin.');
  }
  await sendAdminMenu(ctx);
});

bot.command('helpadmin', async (ctx) => {
  if (!adminIds.includes(ctx.from.id)) return ctx.reply('🚫 Tidak ada izin.');
  
  const helpMsg = `
*📋 Daftar Perintah Admin:*

1. /addsaldo - Tambah saldo user
2. /addserver - Tambah server VPN biasa
3. /addserver_zivpn - Tambah server ZIVPN UDP
4. /addressel - Tambah reseller
5. /delressel - Hapus reseller
6. /listressel - Lihat daftar reseller
7. /broadcast - Kirim pesan ke semua user
8. /backup - Backup database otomatis
9. /hapuslog - Hapus file log
`;
  ctx.reply(helpMsg, { parse_mode: 'Markdown' });
});

// ================= MAIN MENU =================
async function sendMainMenu(ctx) {
  const userId = ctx.from.id;
  const userName = ctx.from.first_name || '-';
  
  // Get user data
  let saldo = 0;
  db.get('SELECT saldo FROM users WHERE user_id = ?', [userId], (err, row) => {
    if (row) saldo = row.saldo;
  });

  const isReseller = await isUserReseller(userId);
  const statusReseller = isReseller ? 'Reseller' : 'Member';

  const messageText = `
╭─ <b>⚡ ${NAMA_STORE} ⚡</b>
├ Bot VPN Premium dengan sistem otomatis
├ Layanan: SSH, VMess, VLess, Trojan, ZIVPN UDP
└────────────────────

<b>👋 Hai, <code>${userName}</code>!</b>
ID: <code>${userId}</code>
Saldo: <code>Rp ${saldo.toLocaleString()}</code>
Status: <code>${statusReseller}</code>

━━━━━━━━━━━━━━━━━━━
<b>📞 KONTAK ADMIN</b>
Telegram: ${ADMIN_CONTACT}
WhatsApp: ${ADMIN_WA}
━━━━━━━━━━━━━━━━━━━

⚙️ <b>MENU LAYANAN</b>`;

  const keyboard = [
    [
      { text: '🌐 VPN Biasa (SSH/VMess/VLess/Trojan)', callback_data: 'menu_vpn' },
      { text: '⚡ ZIVPN UDP', callback_data: 'menu_zivpn' }
    ],
    [
      { text: '💰 TopUp Saldo', callback_data: 'topup_manual' },
      { text: '🤝 Jadi Reseller', callback_data: 'jadi_reseller' }
    ],
    [
      { text: '📊 Cek Server', callback_data: 'cek_service' }
    ]
  ];

  if (ctx.updateType === 'callback_query') {
    await ctx.editMessageText(messageText, {
      parse_mode: 'HTML',
      reply_markup: { inline_keyboard: keyboard }
    }).catch(() => {});
  } else {
    await ctx.reply(messageText, {
      parse_mode: 'HTML',
      reply_markup: { inline_keyboard: keyboard }
    });
  }
}

// ================= MENU VPN BIASA =================
bot.action('menu_vpn', async (ctx) => {
  const keyboard = [
    [
      { text: '➕ Buat Akun', callback_data: 'vpn_create' },
      { text: '♻️ Perpanjang', callback_data: 'vpn_renew' }
    ],
    [
      { text: '❌ Hapus Akun', callback_data: 'vpn_del' },
      { text: '🔒 Kunci Akun', callback_data: 'vpn_lock' }
    ],
    [
      { text: '🔓 Buka Kunci', callback_data: 'vpn_unlock' },
      { text: '🔄 Change IP', callback_data: 'vpn_changeip' }
    ],
    [
      { text: '⌛ Trial', callback_data: 'vpn_trial' },
      { text: '🔧 Fix Akun', callback_data: 'vpn_fix' }
    ],
    [{ text: '🔙 Kembali', callback_data: 'send_main_menu' }]
  ];

  await ctx.editMessageText('🌐 *Pilih Layanan VPN Biasa:*', {
    parse_mode: 'Markdown',
    reply_markup: { inline_keyboard: keyboard }
  });
});

// ================= MENU ZIVPN UDP =================
bot.action('menu_zivpn', async (ctx) => {
  const keyboard = [
    [
      { text: '➕ Buat Akun', callback_data: 'zivpn_create' },
      { text: '♻️ Perpanjang', callback_data: 'zivpn_renew' }
    ],
    [
      { text: '❌ Hapus Akun', callback_data: 'zivpn_del' },
      { text: '⌛ Trial', callback_data: 'zivpn_trial' }
    ],
    [{ text: '🔙 Kembali', callback_data: 'send_main_menu' }]
  ];

  await ctx.editMessageText('⚡ *Pilih Layanan ZIVPN UDP:*', {
    parse_mode: 'Markdown',
    reply_markup: { inline_keyboard: keyboard }
  });
});

// ================= TOPUP MANUAL =================
bot.action('topup_manual', async (ctx) => {
  const msg = `
💰 *TOPUP SALDO MANUAL*

Silakan hubungi admin untuk melakukan topup saldo:

📞 *Telegram:* ${ADMIN_CONTACT}
📱 *WhatsApp:* ${ADMIN_WA}

Format pesan:
<code>Topup [jumlah] - User ID: ${ctx.from.id}</code>

Contoh: <code>Topup 50000 - User ID: ${ctx.from.id}</code>

⏱ Proses cepat ±5 menit setelah pembayaran dikonfirmasi.
`;

  await ctx.editMessageText(msg, {
    parse_mode: 'HTML',
    reply_markup: {
      inline_keyboard: [
        [{ text: '🔙 Kembali', callback_data: 'send_main_menu' }]
      ]
    }
  });
});

// ================= JADI RESELLER =================
bot.action('jadi_reseller', async (ctx) => {
  const msg = `
🤝 *MENJADI RESELLER*

Ingin harga spesial? Hubungi admin:

📞 *Telegram:* ${ADMIN_CONTACT}
📱 *WhatsApp:* ${ADMIN_WA}

Minimal deposit: Rp 100.000
Keuntungan: Harga khusus + fitur tambahan

Format pendaftaran:
<code>Mau jadi reseller - User ID: ${ctx.from.id}</code>
`;

  await ctx.editMessageText(msg, {
    parse_mode: 'HTML',
    reply_markup: {
      inline_keyboard: [
        [{ text: '🔙 Kembali', callback_data: 'send_main_menu' }]
      ]
    }
  });
});

// ================= HANDLER UNTUK VPN BIASA =================
// (Saya akan tambahkan handler lengkap dari bot pertama)
// Contoh untuk create VPN:
bot.action('vpn_create', async (ctx) => {
  const keyboard = [
    [{ text: 'SSH/OpenVPN', callback_data: 'create_ssh' }],
    [{ text: 'VMess', callback_data: 'create_vmess' }, { text: 'VLess', callback_data: 'create_vless' }],
    [{ text: 'Trojan', callback_data: 'create_trojan' }, { text: '🔙 Kembali', callback_data: 'menu_vpn' }]
  ];
  
  await ctx.editMessageText('📋 *Pilih jenis akun VPN:*', {
    parse_mode: 'Markdown',
    reply_markup: { inline_keyboard: keyboard }
  });
});

// ================= HANDLER UNTUK ZIVPN =================
bot.action('zivpn_create', async (ctx) => {
  await startSelectServerZi(ctx, 'create');
});

bot.action('zivpn_renew', async (ctx) => {
  await startSelectServerZi(ctx, 'renew');
});

bot.action('zivpn_del', async (ctx) => {
  await startSelectServerZi(ctx, 'del');
});

bot.action('zivpn_trial', async (ctx) => {
  await startSelectServerZi(ctx, 'trial');
});

// ================= FUNGSI SELECT SERVER ZIVPN =================
async function startSelectServerZi(ctx, action, page = 0) {
  const isR = await isUserReseller(ctx.from.id);
  
  db.all('SELECT * FROM ServerZiVPN', [], (err, servers) => {
    if (err || servers.length === 0) {
      return ctx.reply('⚠️ Belum ada server ZIVPN tersedia.');
    }

    const filteredServers = servers.filter(s => {
      if (s.is_reseller_only && !isR) return false;
      if (!s.is_reseller_only && isR) return false;
      return true;
    });

    const serversPerPage = 5;
    const totalPages = Math.ceil(filteredServers.length / serversPerPage);
    const currentPage = Math.min(page, totalPages - 1);
    const start = currentPage * serversPerPage;
    const currentServers = filteredServers.slice(start, start + serversPerPage);

    const keyboard = [];
    currentServers.forEach(s => {
      keyboard.push([{
        text: `${s.nama_server} - Rp${s.harga}/hari`,
        callback_data: `${action}_ziusername_${s.id}`
      }]);
    });

    const navButtons = [];
    if (currentPage > 0) navButtons.push({ text: '⬅️', callback_data: `zinav_${action}_${currentPage - 1}` });
    if (currentPage < totalPages - 1) navButtons.push({ text: '➡️', callback_data: `zinav_${action}_${currentPage + 1}` });
    if (navButtons.length) keyboard.push(navButtons);
    keyboard.push([{ text: '🔙 Kembali', callback_data: 'menu_zivpn' }]);

    ctx.editMessageText(`📋 *Pilih Server ZIVPN (Halaman ${currentPage + 1}/${totalPages})*`, {
      parse_mode: 'Markdown',
      reply_markup: { inline_keyboard: keyboard }
    });
  });
}

// ================= HANDLER INPUT TEXT =================
bot.on('text', async (ctx) => {
  const state = userState[ctx.chat.id];
  if (!state) return;

  const text = ctx.message.text.trim();

  // Handle input untuk ZIVPN
  if (state.step === 'ziusername') {
    state.username = text;
    if (state.action === 'create' || state.action === 'renew') {
      if (state.type === 'ssh') {
        state.step = 'zipassword';
        await ctx.reply('🔑 *Masukkan password:*', { parse_mode: 'Markdown' });
      } else {
        state.step = 'ziexp';
        await ctx.reply('⏳ *Masukkan masa aktif (hari):*', { parse_mode: 'Markdown' });
      }
    } else if (state.action === 'del') {
      // Untuk delete, password = username
      await processZiAction(ctx, state);
    }
  } else if (state.step === 'zipassword') {
    state.password = text;
    state.step = 'ziexp';
    await ctx.reply('⏳ *Masukkan masa aktif (hari):*', { parse_mode: 'Markdown' });
  } else if (state.step === 'ziexp') {
    const exp = parseInt(text);
    if (isNaN(exp) || exp < 1 || exp > 365) {
      return ctx.reply('❌ *Masa aktif harus angka 1-365.*');
    }
    state.exp = exp;
    await processZiAction(ctx, state);
  }
});

// ================= PROSES ACTION ZIVPN =================
async function processZiAction(ctx, state) {
  const { action, serverId, username, password, exp } = state;
  
  // Cek saldo untuk create/renew
  if (action === 'create' || action === 'renew') {
    db.get('SELECT harga FROM ServerZiVPN WHERE id = ?', [serverId], (err, server) => {
      if (err || !server) return ctx.reply('❌ Server tidak ditemukan.');
      
      const totalHarga = server.harga * exp;
      db.get('SELECT saldo FROM users WHERE user_id = ?', [ctx.from.id], (err, user) => {
        if (!user || user.saldo < totalHarga) {
          return ctx.reply('❌ Saldo tidak mencukupi. Silakan topup.');
        }

        // Proses pembuatan akun
        let func;
        if (action === 'create') func = ziCreate.createssh;
        else if (action === 'renew') func = ziRenew.renewssh;

        func(username, password, exp, 1, serverId).then(async (msg) => {
          if (!msg.includes('❌')) {
            // Kurangi saldo
            db.run('UPDATE users SET saldo = saldo - ? WHERE user_id = ?', [totalHarga, ctx.from.id]);
            
            // Catat transaksi
            db.run('INSERT INTO transactions (user_id, amount, type, reference_id, timestamp) VALUES (?, ?, ?, ?, ?)',
              [ctx.from.id, totalHarga, `zivpn_${action}`, `zi-${Date.now()}`, Date.now()]);
          }
          await ctx.reply(msg, { parse_mode: 'Markdown' });
          delete userState[ctx.chat.id];
        });
      });
    });
  } else if (action === 'del') {
    ziDel.delssh(username, password, 0, 0, serverId).then(msg => {
      ctx.reply(msg, { parse_mode: 'Markdown' });
      delete userState[ctx.chat.id];
    });
  } else if (action === 'trial') {
    const isR = await isUserReseller(ctx.from.id);
    if (!isR) {
      const sudahTrial = await checkTrialAccess(ctx.from.id);
      if (sudahTrial) {
        return ctx.reply('❌ Anda sudah menggunakan trial hari ini.');
      }
      await saveTrialAccess(ctx.from.id);
    }
    
    ziTrial.trialssh('trial-' + Date.now().toString().slice(-5), 'none', '90', '2', serverId).then(async (msg) => {
      await ctx.reply(msg, { parse_mode: 'Markdown' });
      delete userState[ctx.chat.id];
    });
  }
}

// ================= ADMIN MENU =================
async function sendAdminMenu(ctx) {
  const keyboard = [
    [{ text: '➕ Tambah Server VPN', callback_data: 'addserver' }],
    [{ text: '➕ Tambah Server ZIVPN', callback_data: 'addserver_zivpn' }],
    [{ text: '❌ Hapus Server', callback_data: 'deleteserver' }],
    [{ text: '💵 Tambah Saldo User', callback_data: 'addsaldo_user' }],
    [{ text: '📋 List Server', callback_data: 'listserver' }],
    [{ text: '👥 Manajemen Reseller', callback_data: 'menu_reseller' }],
    [{ text: '💾 Backup Database', callback_data: 'backup_now' }],
    [{ text: '🔙 Kembali', callback_data: 'send_main_menu' }]
  ];

  await ctx.editMessageText('🔑 *Menu Admin*', {
    parse_mode: 'Markdown',
    reply_markup: { inline_keyboard: keyboard }
  });
}

// ================= BACKUP OTOMATIS =================
bot.action('backup_now', async (ctx) => {
  if (!adminIds.includes(ctx.from.id)) return;
  
  await ctx.reply('⏳ Melakukan backup database...');
  exec('bash backup.sh', (error, stdout) => {
    if (error) {
      ctx.reply('❌ Backup gagal: ' + error.message);
    } else {
      ctx.reply('✅ Backup selesai!\n' + stdout);
    }
  });
});

// Command backup manual
bot.command('backup', async (ctx) => {
  if (!adminIds.includes(ctx.from.id)) return;
  exec('bash backup.sh', (error, stdout) => {
    ctx.reply(error ? '❌ Backup gagal' : '✅ Backup selesai');
  });
});

// ================= ADD SALDO (manual) =================
bot.command('addsaldo', async (ctx) => {
  if (!adminIds.includes(ctx.from.id)) return;
  
  const args = ctx.message.text.split(' ');
  if (args.length !== 3) {
    return ctx.reply('Format: /addsaldo <user_id> <jumlah>');
  }
  
  const targetId = parseInt(args[1]);
  const amount = parseInt(args[2]);
  
  db.run('UPDATE users SET saldo = saldo + ? WHERE user_id = ?', [amount, targetId], function(err) {
    if (err) return ctx.reply('❌ Gagal: ' + err.message);
    if (this.changes === 0) {
      db.run('INSERT INTO users (user_id, saldo) VALUES (?, ?)', [targetId, amount]);
    }
    ctx.reply(`✅ Saldo Rp${amount} berhasil ditambahkan ke user ${targetId}`);
  });
});

// ================= CEK SERVER =================
bot.action('cek_service', async (ctx) => {
  exec('bash cek-port.sh', (error, stdout) => {
    const cleanOutput = stdout.replace(/\x1b\[[0-9;]*m/g, '');
    ctx.reply(`📡 *Status Server:*\n\`\`\`\n${cleanOutput}\n\`\`\``, { parse_mode: 'Markdown' });
  });
});

// ================= START BOT =================
app.listen(port, () => {
  bot.launch().then(() => {
    logger.info('Bot telah dimulai');
    
    // Backup otomatis SETIAP 6 JAM (00:00, 06:00, 12:00, 18:00)
    exec('(crontab -l 2>/dev/null; echo "0 */6 * * * /usr/bin/bash /root/Botresseler/backup.sh") | crontab -');
    
    logger.info('✅ Backup otomatis dijadwalkan setiap 6 jam (00:00, 06:00, 12:00, 18:00)');
  }).catch((error) => {
    logger.error('Error saat memulai bot:', error);
  });
  logger.info(`Server berjalan di port ${port}`);
});
