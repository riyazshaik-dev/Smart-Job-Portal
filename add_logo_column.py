import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE jobs ADD COLUMN logo TEXT")

conn.commit()
conn.close()

print("Logo column added")