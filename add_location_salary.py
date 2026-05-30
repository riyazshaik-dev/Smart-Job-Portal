import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE jobs ADD COLUMN location TEXT")
cursor.execute("ALTER TABLE jobs ADD COLUMN salary TEXT")

conn.commit()
conn.close()

print("Location and Salary added successfully")