import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM users").fetchall()
print(rows)

conn.close()