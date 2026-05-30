import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# add category column
cursor.execute("ALTER TABLE jobs ADD COLUMN category TEXT")

# add description column
cursor.execute("ALTER TABLE jobs ADD COLUMN description TEXT")

# add location column
cursor.execute("ALTER TABLE jobs ADD COLUMN location TEXT")

# add salary column
cursor.execute("ALTER TABLE jobs ADD COLUMN salary TEXT")

conn.commit()
conn.close()

print("Jobs table updated successfully!")