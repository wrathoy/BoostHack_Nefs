import sqlite3
import hashlib

# Hashing function using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User input
username = 'john_doe'
email = 'john@example.com'
password = 'securepassword123'
hashed_password = hash_password(password)

# Connect to SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert hashed user
cursor.execute('''
INSERT INTO users (username, email, password)
VALUES (?, ?, ?)
''', (username, email, hashed_password))

conn.commit()
conn.close()

print("User inserted with hashed password!")
