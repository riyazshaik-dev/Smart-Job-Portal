import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE saved_jobs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
job_id INTEGER
)
""")

conn.commit()
conn.close()

print("Saved jobs table created")