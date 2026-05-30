import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Users
cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

# Jobs
cursor.execute("""
CREATE TABLE jobs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
company TEXT,
category TEXT,
description TEXT,
location TEXT,
salary TEXT
)
""")

# Applications
cursor.execute("""
CREATE TABLE applications(
id INTEGER PRIMARY KEY AUTOINCREMENT,
job_id INTEGER,
resume TEXT,
status TEXT
)
""")

# ✅ ADD THIS (IMPORTANT)
cursor.execute("""
CREATE TABLE saved_jobs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
job_id INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully ✅")