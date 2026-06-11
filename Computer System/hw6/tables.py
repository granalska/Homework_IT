import sqlite3

conn = sqlite3.connect("mydb.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fullname VARCHAR(100), email VARCHAR(100) UNIQUE);""")

conn.commit()
cur.close()
conn.close()

print("Таблиця створена")