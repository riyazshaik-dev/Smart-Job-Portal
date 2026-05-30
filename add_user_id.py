import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Add user_id to applications table
try:
    cursor.execute("ALTER TABLE applications ADD COLUMN user_id INTEGER")
except:
    print("applications: user_id already exists")

# Add user_id to saved_jobs table
try:
    cursor.execute("ALTER TABLE saved_jobs ADD COLUMN user_id INTEGER")
except:
    print("saved_jobs: user_id already exists")

conn.commit()
conn.close()

print("user_id column added successfully")