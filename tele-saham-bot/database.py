import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Tabel users
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                     username TEXT,
                     first_name TEXT,
                     join_date TEXT,
                     preferences TEXT)''')
        
        # Tabel watchlist
        c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     saham_code TEXT,
                     target_price REAL,
                     created_at TEXT,
                     FOREIGN KEY(user_id) REFERENCES users(user_id))''')
        
        # Tabel notifikasi
        c.execute('''CREATE TABLE IF NOT EXISTS notifications
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     saham_code TEXT,
                     condition TEXT,
                     value REAL,
                     is_active INTEGER DEFAULT 1,
                     created_at TEXT)''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username, first_name):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''INSERT OR IGNORE INTO users 
                    (user_id, username, first_name, join_date, preferences)
                    VALUES (?, ?, ?, ?, ?)''',
                    (user_id, username, first_name, 
                     datetime.now().isoformat(), json.dumps({})))
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    
    def add_to_watchlist(self, user_id, saham_code, target_price=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''INSERT INTO watchlist 
                    (user_id, saham_code, target_price, created_at)
                    VALUES (?, ?, ?, ?)''',
                    (user_id, saham_code.upper(), target_price,
                     datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_watchlist(self, user_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT saham_code, target_price, created_at 
                    FROM watchlist WHERE user_id = ?''', (user_id,))
        watchlist = c.fetchall()
        conn.close()
        return watchlist

db = Database('saham_bot.db')
