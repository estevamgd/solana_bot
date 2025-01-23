import sqlite3
from config import DB_FILE


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            user_id INTEGER PRIMARY KEY,
            public_key TEXT NOT NULL,
            private_key TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_user_wallet(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT public_key, private_key FROM wallets WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def store_wallet(user_id, public_key, private_key):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO wallets (user_id, public_key, private_key) VALUES (?, ?, ?)",
        (user_id, public_key, private_key)
    )
    conn.commit()
    conn.close()
