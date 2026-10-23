import sqlite3

def initialize_database():
    conn = sqlite3.connect("bot_stock.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bots (
        token TEXT PRIMARY KEY,
        bot_type TEXT NOT NULL,
        status TEXT DEFAULT 'available',
        assigned_guild TEXT,
        target_channel TEXT,
        expires_at TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully! Your bot stock structure is ready.")

if __name__ == "__main__":
    initialize_database()
