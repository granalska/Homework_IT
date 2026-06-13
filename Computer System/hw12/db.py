import sqlite3

db = "messages.db"

def init_db():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)""")
    conn.commit()
    conn.close()


def save_message(text):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO messages (text) VALUES(?)", (text,))
    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT text FROM messages")
    data = c.fetchall()
    conn.close()
    return [row[0] for row in data]