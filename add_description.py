import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE jobs ADD COLUMN description TEXT")

conn.commit()
conn.close()

print("Description column added")