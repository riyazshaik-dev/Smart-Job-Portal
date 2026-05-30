import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE applications(
id INTEGER PRIMARY KEY AUTOINCREMENT,
job_id INTEGER
)
""")

conn.commit()
conn.close()

print("applications table created successfully")